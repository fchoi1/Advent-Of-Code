const fs = require("fs");

class RunRAM {
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
    this.grid = this.getInput();

    [this.start, this.end] = this.getLoc();
    this.h = this.grid.length;
    this.w = this.grid[0].length;
    this.dir = [
      [0, 1],
      [1, 0],
      [0, -1],
      [-1, 0],
    ];
    this.save = useTest ? 2 : 100;
    this.costMap = this.fillGrid();
    this.totalSteps = this.costMap.get(`${this.end[0]},${this.end[1]}`);
  }

  getLoc() {
    let start, end;
    for (let j = 0; j < this.grid.length; j++) {
      for (let i = 0; i < this.grid[0].length; i++) {
        if (this.grid[j][i] === "S") start = [i, j];
        if (this.grid[j][i] === "E") end = [i, j];
      }
    }
    return [start, end];
  }

  findValid(start, range) {
    const q = [[start, 0]]; // coord, steps
    const visited = new Set();
    const validTrack = new Map();
    while (q.length) {
      const [curr, steps] = q.shift();
      const [x, y] = curr;
      if (steps > range) continue;
      if ((x != start[0] || y != start[1]) && this.grid[y][x] !== "#") {
        if (
          this.costMap.get(`${x},${y}`) >
          this.costMap.get(`${start[0]},${start[1]}`)
        ) {
          validTrack.set(`${x},${y}`, steps);
        }
      }

      for (const [dx, dy] of this.dir) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx < 0 || nx >= this.w || ny < 0 || ny >= this.h) continue;
        if (visited.has(`${nx},${ny}`)) continue;
        visited.add(`${nx},${ny}`);
        q.push([[nx, ny], steps + 1]);
      }
    }
    return validTrack;
  }

  fillGrid() {
    const costMap = new Map();
    const q = [[this.start, 0]];
    const visited = new Set([`${this.start[0]},${this.start[1]}`]);

    while (q.length) {
      const [curr, steps] = q.shift();
      const [x, y] = curr;
      costMap.set(`${x},${y}`, steps);

      for (const [dx, dy] of this.dir) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx < 0 || nx >= this.w || ny < 0 || ny >= this.h) continue;
        if (this.grid[ny][nx] === "#") continue;
        if (visited.has(`${nx},${ny}`)) continue;
        visited.add(`${nx},${ny}`);
        q.push([[nx, ny], steps + 1]);
      }
    }
    return costMap;
  }

  getSteps(isPart2 = false) {
    const save = {};
    const range = isPart2 ? 20 : 2;
    if (isPart2) this.save = this.useTest ? 50 : 100;

    let count = 0;

    for (let j = 1; j < this.h - 1; j++) {
      for (let i = 1; i < this.w - 1; i++) {
        if (this.grid[j][i] === "E" || this.grid[j][i] === "#") continue;

        const validTrack = this.findValid([i, j], range);

        for (const [key, steps] of validTrack) {
          const [x, y] = key.split(",").map((x) => parseInt(x));

          const startSteps = this.costMap.get(`${i},${j}`);
          const endSteps = this.costMap.get(`${x},${y}`);
          const tripSteps = startSteps + steps + this.totalSteps - endSteps;
          const diff = this.totalSteps - tripSteps;

          if (diff >= this.save) {
            if (!save[diff]) save[diff] = 1;
            else save[diff]++;
            count += 1;
          }
        }
      }
    }

    return Object.values(save).reduce((a, b) => a + b, 0);
  }
}

const runRAM = new RunRAM();
console.log("Day 20 part 1:", runRAM.getSteps());
console.log("Day 20 part 2:", runRAM.getSteps(true));
// Total Runtime ~3.4s
