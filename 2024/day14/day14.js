const fs = require("fs");

class RestroomRedoubt {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => {
        const [posStr, velStr] = row.split(" ");
        const pos = posStr.split("=")[1].split(",").map(Number);
        const vel = velStr.split("=")[1].split(",").map(Number);
        return { pos, vel };
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.w = useTest ? 11 : 101;
    this.h = useTest ? 7 : 103;
    this.robots = this.getInput();
  }

  countQuad(robots) {
    const quadrant = [0, 0, 0, 0];
    for (const { pos } of robots) {
      const [x, y] = pos;
      if (
        x >= 0 &&
        x < Math.floor(this.w / 2) &&
        y >= 0 &&
        y < Math.floor(this.h / 2)
      ) {
        quadrant[0] += 1;
      } else if (
        x >= Math.floor(this.w / 2) + 1 &&
        x < this.w &&
        y >= 0 &&
        y < Math.floor(this.h / 2)
      ) {
        quadrant[1] += 1;
      } else if (
        x >= 0 &&
        x < Math.floor(this.w / 2) &&
        y >= Math.floor(this.h / 2) + 1 &&
        y < this.h
      ) {
        quadrant[2] += 1;
      } else if (
        x >= Math.floor(this.w / 2) + 1 &&
        x < this.w &&
        y >= Math.floor(this.h / 2) + 1 &&
        y < this.h
      ) {
        quadrant[3] += 1;
      }
    }
    return quadrant;
  }

  updateRobots(robots) {
    for (let j = 0; j < robots.length; j++) {
      const { pos, vel } = robots[j];
      const [x, y] = pos;
      const [vx, vy] = vel;
      const newX = (this.w + x + vx) % this.w;
      const newY = (this.h + y + vy) % this.h;
      robots[j] = { pos: [newX, newY], vel };
    }
    return robots;
  }

  runRobots() {
    const time = 10_000;
    let lowest = Infinity;
    let lowestTime = 0;

    let robots = structuredClone(this.robots);

    for (let i = 0; i < time; i++) {
      robots = this.updateRobots(robots);
      const q = this.countQuad(robots);

      const safety = q.reduce((acc, val) => acc * val, 1);
      if (safety < lowest) {
        lowest = safety;
        this.best = structuredClone(robots);
        lowestTime = i + 1;
      }
    }
    return lowestTime;
  }

  displayRobots(robots) {
    const grid = Array(this.h)
      .fill(null)
      .map(() => Array(this.w).fill("."));

    for (const { pos } of robots) {
      const [x, y] = pos;
      grid[y][x] = "X";
    }
    for (let row of grid) {
      console.log(row.join(""));
    }
  }

  process() {
    let robots = structuredClone(this.robots);
    for (let i = 0; i < 100; i++) {
      robots = this.updateRobots(robots);
    }
    const q = this.countQuad(robots);

    this.part1 = q.reduce((acc, val) => acc * val, 1);
    this.part2 = this.runRobots();
  }

  getSF() {
    return this.part1;
  }

  getTime() {
    return this.part2;
  }

  displayTree() {
    this.displayRobots(this.best); // Debug
  }
}

const restroomRedoubt = new RestroomRedoubt();
restroomRedoubt.process();
restroomRedoubt.displayTree();
console.log("Day 14 part 1:", restroomRedoubt.getSF());
console.log("Day 14 part 2:", restroomRedoubt.getTime());
