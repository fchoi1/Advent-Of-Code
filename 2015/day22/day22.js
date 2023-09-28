const fs = require("fs");

class WizardSim {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const boss = {};
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((item) => {
        let [statName, value] = item.split(": ");
        if (statName === "Hit Points") statName = "Health";
        boss[statName] = parseInt(value);
      });
      return boss;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.boss = this.getInput();
    this.you = useTest
      ? {
          Mana: 250,
          Health: 10,
          Armor: 0,
        }
      : {
          Mana: 500,
          Health: 50,
          Armor: 0,
        };
    this.spells = [
      { cost: 53, Damage: 4 },
      { cost: 73, Damage: 2, Health: 2 },
      { cost: 113, effect: 2, turn: 7 }, // shield 7 armor
      { cost: 173, effect: 3, turn: 6 }, // poision deal 3 damage
      { cost: 229, effect: 4, turn: 5 }, // Recharge gain 101 mana
    ];
    this.minMana = Infinity;
    this.seen = new Set();
  }

  // Effects [0,0,0,0,0] for each spell
  playRound(you, boss, manaSpent, effects, currentTurn, hardMode) {
    if (manaSpent > this.minMana) return; // Optimization

    if (currentTurn % 2 === 0 && hardMode) {
      you.Health -= 1;
      if (you.Health <= 0) return;
    }

    // Optimization
    const key = `${you.Mana},${you.Health},${you.Armor},${boss.Health},${effects.join(",")}`;
    if (this.seen.has(key)) return;
    this.seen.add(key);

    const newEffects = effects.map((effect, i) => {
      if (effect > 0) {
        if (i === 2 && effect - 1 === 0) you.Armor -= 7;
        if (i === 3) boss.Health -= 3;
        if (i === 4) you.Mana += 101;
        return effect - 1;
      }
      return effect;
    });

    if (boss.Health <= 0) {
      this.minMana = Math.min(this.minMana, manaSpent);
      return;
    }

    if (currentTurn % 2 === 0) {
      this.spells.forEach((spell, i) => {
        if (newEffects[i] === 0 && you.Mana > spell.cost) {
          const { cost, Damage, Health, effect, turn } = spell;
          const tempYou = { ...you, Mana: you.Mana - cost };
          const tempBoss = { ...boss };

          if (Damage) tempBoss.Health -= Damage;
          if (Health) tempYou.Health += Health;
          if (i === 2) tempYou.Armor += 7;

          const tempEffect = [...newEffects];
          if (effect) tempEffect[effect] = turn;

          this.playRound(tempYou, tempBoss, manaSpent + cost, tempEffect, currentTurn + 1, hardMode);
        }
      });
    } else {
      you.Health -= Math.max(1, boss.Damage - you.Armor);
      if (you.Health < 0) return;
      this.playRound(you, boss, manaSpent, newEffects, currentTurn + 1, hardMode);
    }
  }

  getMinMana(hardMode) {
    this.minMana = Infinity;
    this.playRound(this.you, this.boss, 0, [0, 0, 0, 0, 0], 0, hardMode);
    return this.minMana;
  }
}

const wizardSim = new WizardSim();
console.log("Day 22 part 1:", wizardSim.getMinMana());
console.log("Day 22 part 2:", wizardSim.getMinMana(true));
