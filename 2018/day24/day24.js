const fs = require("fs");

class ImmuneSystem {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const infect = {};
      const immune = {};
      let currGroup;
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((row) => {
        if (!row) return;
        if (row === "Immune System:") return (currGroup = immune);
        if (row === "Infection:") return (currGroup = infect);
        const splitted = row.split(" ");
        const id = parseInt(splitted.slice(-1)[0]);
        const brackets = row.split(/\(|\)/)[1];
        currGroup[id] = {
          ...this.parseBrackets(!!brackets ? brackets : ""),
          units: parseInt(splitted[0]),
          hp: parseInt(splitted[4]),
          attack: parseInt(splitted.slice(-6)[0]),
          attackType: splitted.slice(-5)[0],
          id,
          type: currGroup === infect ? "infect" : "immune",
        };
      });
      return [immune, infect];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.immune, this.infect] = this.getInput();
  }

  parseBrackets(str) {
    const stats = {
      immune: new Set(),
      weak: new Set(),
    };
    str.split("; ").forEach((stat) => {
      const split = stat.split(/, | /);
      split.slice(2).forEach((attr) => stats[split[0]].add(attr));
    });
    return stats;
  }

  selectTargets(attack, defendObj) {
    if (!defendObj) return [attack.id, null];
    let defend = null;
    for (const d of this.getOrder(defendObj)) {
      if (d.immune.has(attack.attackType)) continue;
      if (d.weak.has(attack.attackType)) {
        defend = d;
        break;
      }
      if (!defend) defend = d;
    }
    if (defend !== null) delete defendObj[defend.id];
    return [attack, defend];
  }

  attackTargets(attack, defend) {
    if (!attack || !defend) return false;
    const defenders = attack.type === "immune" ? this.infect : this.immune;
    const attackers = attack.type === "immune" ? this.immune : this.infect;
    if (!attackers[attack.id]) return false;
    const dmg = defend.weak.has(attack.attackType) ? 2 * attack.units * attack.attack : attack.units * attack.attack;
    const updatedUnits = defend.units - Math.floor(dmg / defend.hp);
    if (updatedUnits <= 0) delete defenders[defend.id];
    else if (defenders[defend.id].units === updatedUnits) return false;
    else defenders[defend.id].units = updatedUnits;
    return true;
  }

  getOrder(groups) {
    return Object.values(groups).sort((a, b) => {
      if (b.units * b.attack === a.units * a.attack) return a.id - b.id;
      return b.units * b.attack - a.units * a.attack;
    });
  }
  getSum() {
    return Object.values({ ...this.immune, ...this.infect }).reduce((prev, curr) => prev + curr.units, 0);
  }

  isDone() {
    return Object.keys(this.immune).length === 0 || Object.keys(this.infect).length === 0;
  }

  runGame(boost) {
    [this.immune, this.infect] = this.getInput();
    for (const group of Object.values(this.immune)) group.attack += boost;

    while (!this.isDone()) {
      const order = [...this.getOrder(this.infect), ...this.getOrder(this.immune)];
      const tempImmune = { ...this.immune };
      const tempInfect = { ...this.infect };
      const attackList = order.map((group) => {
        const defendObj = group.type === "immune" ? tempInfect : tempImmune;
        return this.selectTargets(group, defendObj);
      });
      attackList.sort((a, b) => b[0].id - a[0].id);
      let didAttack = false;
      attackList.forEach(([attack, defend]) => {
        if (this.attackTargets(attack, defend)) didAttack = true;
      });
      if (!didAttack) break;
    }
    const immuneWin = Object.keys(this.immune).length !== 0 && Object.keys(this.infect).length === 0;
    const winGroup = !immuneWin ? this.infect : this.immune;
    return [immuneWin, Object.values(winGroup).reduce((prev, curr) => prev + curr.units, 0)];
  }

  getUnitWin() {
    return this.runGame(0)[1];
  }

  getScore() {
    return Object.values(this.infect).reduce((prev, curr) => prev + curr.units * curr.attack, 0);
  }

  getMinBoost() {
    let boost = 1;
    let immuneWin = false;
    let score;
    while (!immuneWin) {
      [immuneWin, score] = this.runGame(boost);
      if (immuneWin) return score;
      boost++;
    }
  }
}

const immuneSystem = new ImmuneSystem();
console.log("Day 24 part 1:", immuneSystem.getUnitWin());
console.log("Day 24 part 2:", immuneSystem.getMinBoost());
