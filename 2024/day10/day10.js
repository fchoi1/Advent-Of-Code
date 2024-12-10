const fs = require("fs");

class Hiking {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((dimension) => dimension.split("").map(Number));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.grid = this.getInput();
    this.w = this.grid[0].length;
    this.h = this.grid.length;
    this.directions = [
      [0, -1],
      [1, 0],
      [0, 1],
      [-1, 0],
    ];
  }

  bfs(i, j, isPart2 = false) {
    let queue = [[i, j, 0]];
    let visited = new Set();
    let nines = 0;

    while (queue.length > 0) {
      let [x, y, height] = queue.shift();

      if (!isPart2 && visited.has(`${x},${y}`)) continue;
      if (!isPart2) visited.add(`${x},${y}`);

      if (this.grid[y][x] === 9) nines++;

      for (let [dx, dy] of this.directions) {
        let [nx, ny] = [x + dx, y + dy];
        if (nx < 0 || nx >= this.w || ny < 0 || ny >= this.h) continue;
        if (this.grid[ny][nx] === height + 1) {
          queue.push([nx, ny, height + 1]);
        }
      }
    }
    return nines;
  }

  countTrail(isPart2 = false) {
    let count = 0;
    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        if (this.grid[j][i] === 0) count += this.bfs(i, j, isPart2);
      }
    }
    return count;
  }
}

const hiking = new Hiking();
console.log("Day 10 part 1:", hiking.countTrail());
console.log("Day 10 part 2:", hiking.countTrail(true));
