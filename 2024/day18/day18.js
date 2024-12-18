const fs = require("fs");

class RunRAM {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => row.split(",").map(Number));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.bytes = this.getInput();
    this.size = useTest ? 12 : 1024;
    this.end = useTest ? [6, 6] : [70, 70];
    this.h = useTest ? 6 : 70;
    this.w = useTest ? 6 : 70;
    this.dir = [
      [0, 1],
      [1, 0],
      [0, -1],
      [-1, 0],
    ];
  }

  bfs(bytes) {
    const q = [[0, 0, 0]];
    const visited = new Set();
    while (q.length > 0) {
      const [x, y, steps] = q.shift();
      const key = `${x},${y}`;

      if (x === this.end[0] && y === this.end[1]) return steps;

      if (visited.has(key)) continue;
      visited.add(key);

      for (const [dx, dy] of this.dir) {
        const newX = x + dx;
        const newY = y + dy;
        if (newX < 0 || newX > this.w || newY < 0 || newY > this.h) continue;
        const newKey = `${newX},${newY}`;
        if (bytes.has(newKey)) continue;

        q.push([newX, newY, steps + 1]);
      }
    }
    return -1;
  }

  process() {
    const bytes = new Set();

    for (let b of this.bytes.slice(0, this.size)) {
      bytes.add(`${b[0]},${b[1]}`);
    }

    this.part1 = this.bfs(bytes);

    for (let b of this.bytes.slice(this.size)) {
      bytes.add(`${b[0]},${b[1]}`);
      const steps = this.bfs(bytes);
      if (steps < 0) {
        this.part2 = `${b[0]},${b[1]}`;
        break;
      }
    }
  }

  getSteps() {
    return this.part1;
  }
  getByte() {
    return this.part2;
  }
}

const runRAM = new RunRAM();
runRAM.process();
console.log("Day 18 part 1:", runRAM.getSteps());
console.log("Day 18 part 2:", runRAM.getByte());
// Total Runtime ~2.5s
