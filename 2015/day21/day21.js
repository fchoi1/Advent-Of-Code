const fs = require("fs");

class RPG {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const boss = {};
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
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
          Health: 8,
          Damage: 5,
          Armor: 5,
        }
      : {
          Health: 100,
          Damage: 0,
          Armor: 0,
        };
    this.shop = [
      [
        { cost: 8, Damage: 4, Armor: 0 },
        { cost: 10, Damage: 5, Armor: 0 },
        { cost: 25, Damage: 6, Armor: 0 },
        { cost: 40, Damage: 7, Armor: 0 },
        { cost: 74, Damage: 8, Armor: 0 },
      ],
      [
        { cost: 13, Damage: 0, Armor: 1 },
        { cost: 31, Damage: 0, Armor: 2 },
        { cost: 53, Damage: 0, Armor: 3 },
        { cost: 75, Damage: 0, Armor: 4 },
        { cost: 102, Damage: 0, Armor: 5 },
      ],
      [
        { cost: 20, Damage: 0, Armor: 1 },
        { cost: 25, Damage: 1, Armor: 0 },
        { cost: 40, Damage: 0, Armor: 2 },
        { cost: 50, Damage: 2, Armor: 0 },
        { cost: 80, Damage: 0, Armor: 3 },
        { cost: 100, Damage: 3, Armor: 0 },
      ],
    ];
    this.maxGold = 180 + 102 + 74;
    this.minWinGold = this.maxGold;
    this.maxLoseGold = 0;
    this.seen = new Set();
    this.playAllgames();
  }

  playRound(attack, defend) {
    defend.Health -= Math.max(1, attack.Damage - defend.Armor);
    return [attack, defend];
  }

  isWinner(boss, you) {
    let turn = 0;
    while (you.Health > 0 && boss.Health > 0) {
      if (turn % 2 === 0) [you, boss] = this.playRound(you, boss);
      else [boss, you] = this.playRound(boss, you);
      turn++;
    }
    return you.Health > 0;
  }

  getConfigurations(gold, configuration, category, configList) {
    if (category >= 3 || gold < 8) {
      const key = configuration.join(",");
      if (this.seen.has(key)) return configList;
      else {
        this.seen.add(key);
        configList.push(configuration);
        return configList;
      }
    }
    configList = this.getConfigurations(gold, configuration, category + 1, configList);

    this.shop[category].forEach((item, i) => {
      const newConfig = [...configuration];
      if (category === 2) {
        if (gold >= item.cost) {
          newConfig[category] = i;
          const newGold = gold - item.cost;
          configList = this.getConfigurations(newGold, newConfig, 3, configList);

          if (i < this.shop[category].length - 1) {
            this.shop[category].slice(i + 1).forEach((item, index) => {
              if (newGold >= item.cost) {
                newConfig[category + 1] = index + i + 1;
                configList = this.getConfigurations(newGold - item.cost, newConfig, 3, configList);
              }
            });
          }
        }
      } else if (gold >= item.cost) {
        newConfig[category] = i;
        configList = this.getConfigurations(gold - item.cost, newConfig, category + 1, configList);
      }
    });
    return configList;
  }

  playAllgames() {
    let gold = 0;
    while (gold <= this.maxGold + 1) {
      const configList = this.getConfigurations(gold, new Array(4), 0, []);
      if (configList.length === 0) {
        gold += 1;
        continue;
      }
      for (const config of configList) {
        const newYou = { ...this.you };
        if (config[0] === undefined) continue; // Weapon is mandatory

        config.forEach((val, i) => {
          if (val !== undefined) {
            const index = i == 3 ? i - 1 : i;
            const { Damage, Armor } = this.shop[index][val];
            newYou.Damage += Damage;
            newYou.Armor += Armor;
          }
        });
        const result = this.isWinner({ ...this.boss }, newYou);
        if (result) this.minWinGold = Math.min(this.minWinGold, gold);
        else this.maxLoseGold = Math.max(this.maxLoseGold, gold);
      }
      gold += 1;
    }
  }

  getLeastWinGold() {
    return this.minWinGold;
  }

  getMostLoseGold() {
    return this.maxLoseGold;
  }
}

const rpg = new RPG();
console.log("Day 21 part 1:", rpg.getLeastWinGold());
console.log("Day 21 part 2:", rpg.getMostLoseGold());
