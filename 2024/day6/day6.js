const fs = require("fs");

class Report {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((line) => {
        return line.split("");
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.grid = this.getInput();
    this.w = this.grid[0].length;
    this.h = this.grid.length;
    this.start = this.getStart();
    this.directions = [
      [0, -1],
      [1, 0],
      [0, 1],
      [-1, 0],
    ];
    this.originalPath = this.getOriginalPath();
  }

  getStart() {
    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        if (this.grid[j][i] === "^") return [i, j];
      }
    }
  }

  getOriginalPath() {
    let curr = 0;
    const seen = new Set();
    let [x, y] = this.start;
    while (x >= 0 && x < this.w && y >= 0 && y < this.h) {
      seen.add(`${x},${y}`);
      const [dx, dy] = this.directions[curr];
      if (x + dx < 0 || x + dx >= this.w || y + dy < 0 || y + dy >= this.h)
        break;

      if (this.grid[y + dy][x + dx] === "#") {
        curr = (curr + 1) % 4;
      } else {
        x += dx;
        y += dy;
      }
    }
    return seen;
  }

  runGuard() {
    let curr = 0;
    const seen = new Set();
    const uniqueSeen = new Set();
    let [x, y] = this.start;
    while (x >= 0 && x < this.w && y >= 0 && y < this.h) {
      seen.add(`${x},${y}`);
      const [dx, dy] = this.directions[curr];
      const key = `${x},${y},${dx},${dy}`;
      if (uniqueSeen.has(key)) return -1;
      uniqueSeen.add(key);
      if (x + dx < 0 || x + dx >= this.w || y + dy < 0 || y + dy >= this.h)
        break;

      if (this.grid[y + dy][x + dx] === "#") {
        curr = (curr + 1) % 4;
      } else {
        x += dx;
        y += dy;
      }
    }
    return seen.size;
  }

  countDistinct() {
    return this.originalPath.size;
  }

  isAffected(x, y) {
    for (let i = 0; i < this.directions.length; i++) {
      const [dx, dy] = this.directions[i];
      const key = `${x + dx},${y + dy}`;
      if (this.originalPath.has(key)) return true;
    }
    return false;
  }

  getLoopCount() {
    let count = 0;

    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        if (
          this.grid[j][i] === "^" ||
          this.grid[j][i] === "#" ||
          !this.isAffected(i, j)
        )
          continue;
        this.grid[j][i] = "#";
        if (this.runGuard() === -1) count++;
        this.grid[j][i] = ".";
      }
    }
    return count;
  }
}

const report = new Report();
console.log("Day 6 part 1:", report.countDistinct());
console.log("Day 6 part 2:", report.getLoopCount());
// time: ~9.2s
