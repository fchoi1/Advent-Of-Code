const fs = require("fs");

class Maze {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return [
        parseInt(data[0].split(" ")[1]),
        data[1]
          .split(" ")[1]
          .split(",")
          .map((val) => parseInt(val)),
      ];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.depth, this.target] = this.getInput();
    this.cache = {};
    this.map = {};
    this.dirMap = [
      [0, 1],
      [1, 0],
      [0, -1],
      [-1, 0],
    ];
    this.time = Infinity;
    this.seen = new Set();
    this.itemMap = [
      [1, 2],
      [0, 1],
      [0, 2],
    ];
    this.generateMap();
  }

  getGeologic(x, y) {
    if ((x === 0 && y === 0) || (x === this.target[0] && y === this.target[1])) return 0;
    if (y === 0) return x * 16807;
    if (x === 0) return y * 48271;
    return this.getErosionLvl(x - 1, y) * this.getErosionLvl(x, y - 1);
  }

  getErosionLvl(x, y) {
    const key = `${x},${y}`;
    if (this.cache[key]) return this.cache[key];
    this.cache[key] = (this.getGeologic(x, y) + this.depth) % 20183;
    return this.cache[key];
  }

  getType(x, y) {
    const key = `${x},${y}`;
    if (this.map[key]) return this.map[key];
    this.map[key] = this.getErosionLvl(x, y) % 3;
    return this.map[key];
  }

  generateMap() {
    let risk = 0;
    for (let j = 0; j <= this.target[1]; j++) {
      for (let i = 0; i <= this.target[0]; i++) {
        risk += this.getType(i, j);
      }
    }
    this.risk = risk;
  }

  bfs() {
    let q = [[0, 0, 2]];
    let time = 0;
    let isDelayEmpty;
    const delay = Array.from({ length: 7 }, () => []);
    while (q.length > 0 || !isDelayEmpty) {
      let temp = [];
      for (const [x, y, item] of q) {
        const key = `${x},${y},${item}`;
        if (this.seen.has(key)) continue;
        this.seen.add(key);
        if (x === this.target[0] && y === this.target[1] && item == 2) return time;
        else if (x === this.target[0] && y === this.target[1]) return time + 7;

        for (const [dx, dy] of this.dirMap) {
          const [newX, newY] = [x + dx, y + dy];
          if (newX >= 0 && newY >= 0) {
            const type = this.getType(newX, newY);
            if (this.itemMap[item].includes(type)) temp.push([newX, newY, item]);
          }
        }
        const currType = this.getType(x, y);
        const newItem = this.itemMap[currType].find((n) => n !== item);
        if (this.seen.has(`${x},${y},${newItem}`)) continue;
        delay[time % 7].push([x, y, newItem]);
      }
      time++;
      q = [...temp, ...delay[time % 7]];
      delay[time % 7] = [];
      isDelayEmpty = delay.every((innerArray) => innerArray.length === 0);
    }
    return -1;
  }

  getRisk() {
    return this.risk;
  }

  getFastestRoute() {
    return this.bfs();
  }
}

const maze = new Maze();
console.log("Day 22 part 1:", maze.getRisk());
console.log("Day 22 part 2:", maze.getFastestRoute());
