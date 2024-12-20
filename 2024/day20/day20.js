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

    [this.start, this.end] = this.getLoc(this.grid);
    this.save = useTest ? 2 : 100;
    this.h = this.grid.length;
    this.w = this.grid[0].length;
    this.dir = [
      [0, 1],
      [1, 0],
      [0, -1],
      [-1, 0],
    ];

    console.log(this.start, this.end);
    console.log("Dimensions:", this.h, this.w);
  }

  printMap(map) {
    for (const row of map) {
      console.log(row.join(""));
    }
  }

  getLoc(map) {
    let start, end;
    for (let j = 0; j < map.length; j++) {
      for (let i = 0; i < map[0].length; i++) {
        if (map[j][i] === "S") start = [i, j];
        if (map[j][i] === "E") end = [i, j];
      }
    }
    return [start, end];
  }

  getPath(start, end, map) {
    const q = [[start, 0]];
    const visited = new Set();
    while (q.length) {
      const [curr, steps] = q.shift();
      const [x, y] = curr;
      if (x === end[0] && y === end[1]) return steps;

      for (const [dx, dy] of this.dir) {
        const nextX = x + dx;
        const nextY = y + dy;
        if (nextX < 0 || nextX >= this.w || nextY < 0 || nextY >= this.h)
          continue;
        if (map[nextY][nextX] === "#") continue;
        if (visited.has(`${nextX},${nextY}`)) continue;
        visited.add(`${nextX},${nextY}`);
        q.push([[nextX, nextY], steps + 1]);
      }
    }
  }

  fillGrid(start, map) {
    const costMap = new Map();
    const q = [[start, 0]];
    const visited = new Set([`${start[0]},${start[1]}`]);
    while (q.length) {
      const [curr, steps] = q.shift();
      const [x, y] = curr;
      costMap.set(`${x},${y}`, steps);

      for (const [dx, dy] of this.dir) {
        const nextX = x + dx;
        const nextY = y + dy;
        if (nextX < 0 || nextX >= this.w || nextY < 0 || nextY >= this.h)
          continue;
        if (map[nextY][nextX] === "#") continue;
        if (visited.has(`${nextX},${nextY}`)) continue;
        visited.add(`${nextX},${nextY}`);
        q.push([[nextX, nextY], steps + 1]);
      }
    }
    console.log(costMap);
    return costMap;
  }

  getSteps() {
    const steps = this.bfs(this.start, this.end, this.grid);
    console.log("total steps", steps);
    const save = {};

    let count = 0;

    for (let j = 1; j < this.h - 1; j++) {
      for (let i = 1; i < this.w - 1; i++) {
        if (this.grid[j][i] === "E" || this.grid[j][i] === "S") continue;
        if (this.grid[j][i] === ".") continue;
        // right
        let test;

        for (const [dx, dy] of this.dir) {
          const nextX = x + dx;
          const nextY = y + dy;
          if (nextX < 0 || nextX >= this.w || nextY < 0 || nextY >= this.h)
            continue;
          if (this.grid[nextY][nextX] === "#" || nextX == i  ) continue;
        }

      

        this.grid[j][i] = ".";
        // this.grid[j][i + 1] = "X";

        test = this.bfs(this.start, this.end, this.grid);
        const diff = steps - test;
        if (diff >= this.save) {
          // this.printMap(this.grid);
          if (!save[diff]) save[diff] = 1;
          else save[diff]++;
          count += 1;

          // console.log("stesp", test, "Diff", steps - test);
        }
  
      }
    }
    // console.log(save);
    return count;
  }
  getByte() {
    const costMap = this.fillGrid(this.end, this.grid);

    const cellWidth = 5; // Adjust width based on your needs
    for (let j = 0; j < this.h; j++) {
      let str = "";
      for (let i = 0; i < this.w; i++) {
        const key = `${i},${j}`;
        if (costMap.has(key)) {
          str += costMap.get(key).toString().padStart(cellWidth, " ");
        } else {
          str += this.grid[j][i].toString().padStart(cellWidth, " ");
        }
      }
      console.log(str);
    }

    return this.part2;
  }
}

const runRAM = new RunRAM(true);
// console.log("Day 20 part 1:", runRAM.getSteps());
console.log("Day 20 part 2:", runRAM.getByte());
