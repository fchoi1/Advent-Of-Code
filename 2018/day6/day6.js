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
    [this.minWidth, this.width, this.minHeight, this.height] = this.getDimensions();
    this.infinite = this.filterEdges();
    this.grid = {};
    this.updateGrid();
  }

  inBounds([x, y]) {
    return x >= this.minWidth && x < this.width && y >= this.minHeight && y < this.height;
  }

  updateGrid() {
    this.coordList.forEach((element) => {
      this.updateElement(element);
    });
  }

  updateElement(start) {
    let q = [start];
    const visited = new Set();
    const dir = [
      [0, 1],
      [0, -1],
      [1, 0],
      [-1, 0],
    ];
    let step = 0;
    while (q.length !== 0) {
      const temp = [];
      for (const coord of q) {
        const key = `${coord[0]},${coord[1]}`;
        if (visited.has(key)) continue;
        visited.add(key);
        if (!this.grid[key] || step < this.grid[key].step) {
          this.grid[key] = { key: `${start[0]},${start[1]}`, step };
        } else if (this.grid[key] && step === this.grid[key].step) {
          this.grid[key].key = null;
        }
        for (const [dx, dy] of dir) {
          const newCord = [coord[0] + dx, coord[1] + dy];
          if (this.inBounds(newCord)) {
            temp.push(newCord);
          }
        }
      }
      step += 1;
      q = temp;
    }
  }

  getClosest(start) {
    let q = [start];
    const visited = new Set();
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
        const newCords = [];
        newCords.push([coord[0] + 1, coord[1]]);
        newCords.push([coord[0] - 1, coord[1]]);
        newCords.push([coord[0], coord[1] + 1]);
        newCords.push([coord[0], coord[1] + -1]);
        temp.push(...newCords);
      }
      if (found) return closest;
      q = temp;
    }
    return closest;
  }

  getDimensions() {
    return this.coordList.reduce(
      ([minX, maxX, minY, maxY], [x, y]) => [
        Math.min(x, minX),
        Math.max(x, maxX),
        Math.min(y, minY),
        Math.max(y, maxY),
      ],
      [Infinity, 0, Infinity, 0]
    );
  }

  filterEdges() {
    let infinite = new Set();
    for (let i = this.minWidth; i < this.width; i++) {
      const top = this.getClosest([this.minHeight, i]);
      const bot = this.getClosest([this.height, i]);
      if (top.size === 1) infinite = new Set([...infinite, ...top]);
      if (bot.size === 1) infinite = new Set([...infinite, ...bot]);
    }
    for (let i = this.minHeight; i < this.height; i++) {
      const left = this.getClosest([i, this.minWidth]);
      const right = this.getClosest([i, this.width]);
      if (left.size === 1) infinite = new Set([...infinite, ...left]);
      if (right.size === 1) infinite = new Set([...infinite, ...right]);
    }
    return infinite;
  }

  getLargestArea() {
    let currCount = 0;
    let numCounts = {};
    for (const coord of Object.values(this.grid)) {
      if (coord.key && !this.infinite.has(coord.key)) {
        numCounts[coord.key] = numCounts[coord.key] + 1 || 1;
        currCount = Math.max(currCount, numCounts[coord.key]);
      }
    }
    return currCount;
  }

  isUnderDist(x, y, dist) {
    return dist > this.coordList.reduce((prev, curr) => prev + Math.abs(curr[0] - x) + Math.abs(curr[1] - y), 0);
  }

  countRegions() {
    let count = 0;
    const region = this.useTest ? 32 : 10_000;
    for (let i = this.minWidth; i < this.width; i++) {
      for (let j = this.minHeight; j < this.height; j++) {
        if (this.isUnderDist(i, j, region)) count += 1;
      }
    }
    return count;
  }
}

const alchemical = new Alchemical();
console.log("Day 6 part 1:", alchemical.getLargestArea());
console.log("Day 6 part 2:", alchemical.countRegions());
// Total Runtime 7.3s
