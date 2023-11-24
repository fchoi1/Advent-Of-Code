const fs = require("fs");

class LumberYard {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => row.split(""));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.forestMap = this.getInput();
    this.width = this.forestMap[0].length;
    this.height = this.forestMap.length;
  }

  getAcreScore() {
    let lumber = 0;
    let trees = 0;
    this.forestMap.forEach((row) => {
      row.forEach((acre) => {
        if (acre === "#") lumber++;
        else if (acre === "|") trees++;
      });
    });
    return lumber * trees;
  }

  checkAcre(x, y) {
    const dirMap = [
      [0, 1],
      [0, -1],
      [1, 0],
      [-1, 0],
      [1, 1],
      [1, -1],
      [-1, 1],
      [-1, -1],
    ];
    let trees = 0;
    let lumber = 0;
    for (const [dx, dy] of dirMap) {
      const newX = x + dx;
      const newY = y + dy;
      if (newX >= 0 && newX < this.width && newY >= 0 && newY < this.height) {
        if (this.forestMap[newY][newX] === "#") lumber++;
        else if (this.forestMap[newY][newX] === "|") trees++;
      }
    }
    const acre = this.forestMap[y][x];
    if (acre === ".") return trees >= 3 ? "|" : acre;
    else if (acre === "|") return lumber >= 3 ? "#" : acre;
    else if (acre === "#") return trees >= 1 && lumber >= 1 ? "#" : ".";
  }

  getResources(isPart2) {
    this.forestMap = this.getInput();
    let time = 0;
    let maxTime = isPart2 ? 1_000_000_000 : 10;
    const repeated = 5;
    const scoreList = [];
    let score, key;
    const seen = {};
    while (time < maxTime) {
      const temp = [];
      for (let j = 0; j < this.height; j++) {
        const row = [];
        for (let i = 0; i < this.width; i++) row.push(this.checkAcre(i, j));
        temp.push(row);
      }
      this.forestMap = temp;
      score = this.getAcreScore();
      scoreList.push(score);
      key = scoreList.slice(-repeated).join(",");
      time++;
      if (seen[key]) break;
      seen[key] = time;
    }
    if (maxTime === time) return score;
    const loopLength = time - seen[key];
    const looped = scoreList.slice(-loopLength);
    return looped[((maxTime - time) % loopLength) - 1];
  }
}

const lumberYard = new LumberYard();
console.log("Day 18 part 1:", lumberYard.getResources());
console.log("Day 18 part 2:", lumberYard.getResources(true));
