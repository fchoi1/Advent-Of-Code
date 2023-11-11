const fs = require("fs");

class Alchemical {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const coordSet = new Set();
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      const coordList = data.map((coords) => {
        const [x, y] = coords.split(", ");
        coordSet.add(`${x},${y}`);
        return [parseInt(x), parseInt(y)];
      });
      return [coordList, coordSet];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.coordList, this.coordSet] = this.getInput();
    [this.width, this.height] = this.getDimensions();
    this.infinite = this.filterEdges();
    console.log(this.coordList, this.coordSet, [this.width, this.height]);
  }

  getClosest(start) {
    let q = [start];
    const visited = new Set();
    const dir = [
      [0, 1],
      [0, -1],
      [1, 0],
      [-1, 0],
    ];
    const closest = new Set();
    let found = false;
    while (q.length !== 0) {
      const temp = [];
      for (const coord of q) {
        const key = `${coord[0]},${coord[1]}`;
        if (this.coordSet.has(key)) {
          found = true;
          closest.add(key);
        }
        if (visited.has(key)) continue;
        visited.add(key);
        for (const [dx, dy] of dir) {
          const newCord = [coord[0] + dx, coord[1] + dy];
          temp.push(newCord);
        }
      }
      if (found) return closest;
      q = temp;
    }
    return closest;
  }

  getDimensions() {
    let maxX = 0;
    let maxY = 0;
    for (const [x, y] of this.coordList) {
      if (x > maxX) maxX = x;
      if (y > maxY) maxY = y;
    }
    return [maxX, maxY];
  }

  filterEdges() {
    let infinite = new Set();
    for (let i = 0; i < this.width; i++) {
      const bot = this.getClosest([0, i]);
      const top = this.getClosest([this.height, i]);
      if (top.size === 1) infinite = new Set([...infinite, ...top]);
      if (bot.size === 1) infinite = new Set([...infinite, ...bot]);
    }
    for (let i = 0; i < this.hieght; i++) {
      const left = this.getClosest([i, 0]);
      const right = this.getClosest([i, this.width]);
      if (left.size === 1) infinite = new Set([...infinite, ...left]);
      if (right.size === 1) infinite = new Set([...infinite, ...right]);
    }
    return infinite;
  }

  getLargestArea() {
    const counts = {};
    this.coordSet.forEach((element) => {
      if (!this.infinite.has(element)) counts[element] = 0;
    });
    for (let i = 0; i < this.width; i++) {
      console.log("checking", i);
      for (let j = 0; j < this.height; j++) {
        const closest = this.getClosest([i, j]);
        if (closest.size == 1) {
          const coord = closest.values().next().value;
          if (coord in counts) {
            counts[coord] += 1;
          }
        }
      }
    }

    console.log("counts", counts);
  }
}

const alchemical = new Alchemical();
console.log("Day 6 part 1:", alchemical.getLargestArea());
