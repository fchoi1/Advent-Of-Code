const fs = require("fs");

class Maze {
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
    this.map = this.getInput();
    this.directions = [
      [1, 0],
      [0, 1],
      [-1, 0],
      [0, -1],
    ];
    this.getLoc();
    [this.part1, this.part2] = this.bfs();
  }

  getLoc() {
    for (let j = 0; j < this.map.length; j++) {
      for (let i = 0; i < this.map[0].length; i++) {
        if (this.map[j][i] === "S") this.start = [i, j];
        else if (this.map[j][i] === "E") this.end = [i, j];
      }
    }
  }

  bfs() {
    let key = `${this.start[0]},${this.start[1]},${this.directions[0][0]},${this.directions[0][1]}`;
    let q = [[0, 0, this.start, new Set([key])]];
    let visited = new Set();
    let _;

    while (q.length > 0) {
      q.sort((a, b) => {
        if (a[0] !== b[0]) return a[0] - b[0];
        if (a[2][0] !== b[2][0]) return a[2][0] - b[2][0];
        if (a[2][1] !== b[2][1]) return a[2][1] - b[2][1];
        return a[3].size - b[3].size;
      });

      let [score, dir, start, seen] = q.shift();

      // Combine same locations
      while (
        q.length > 0 &&
        q[0][0] === score &&
        q[0][2][0] === start[0] &&
        q[0][2][1] === start[1]
      ) {
        seen = new Set([...seen, ...q[0][3]]);
        [score, dir, start, _] = q.shift();
      }

      const [x, y] = start;
      const [curr_dx, curr_dy] = this.directions[dir];
      key = `${x},${y},${curr_dx},${curr_dy}`;

      if (this.map[y][x] === "E") return [score, seen.size];

      if (visited.has(key)) continue;
      visited.add(key);

      for (const [s, d] of [
        [1001, -1],
        [1, 0],
        [1001, 1],
      ]) {
        const [dx, dy] = this.directions[(dir + 4 + d) % 4];
        if (this.map[y + dy][x + dx] === "#") continue;
        const newSeen = new Set(seen);
        newSeen.add(`${x + dx},${y + dy}`);
        q.push([score + s, (dir + 4 + d) % 4, [x + dx, y + dy], newSeen]);
      }
    }
    return [null, null];
  }
  getScore() {
    return this.part1;
  }
  getTiles() {
    return this.part2;
  }
}

const maze = new Maze();
console.log("Day 16 part 1:", maze.getScore());
console.log("Day 16 part 2:", maze.getTiles());
