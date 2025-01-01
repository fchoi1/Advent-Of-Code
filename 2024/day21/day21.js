const fs = require("fs");

class RunRAM {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.directionKey = [
      ["*", "^", "A"],
      ["<", "v", ">"],
    ];
    this.numberKey = [
      ["7", "8", "9"],
      ["4", "5", "6"],
      ["1", "2", "3"],
      ["*", "0", "A"],
    ];
    this.reversePairs = new Set([
      "A,<",
      "^,<",
      "A,1",
      "A,4",
      "A,7",
      "0,1",
      "0,4",
      "0,7",
    ]);
    this.codes = this.getInput();
    this.dirMap = this.getMap(this.directionKey);
    this.numMap = this.getMap(this.numberKey);
    this.cache = new Map();
    console.log(this.dirMap);
    console.log(this.numMap);
  }

  getMap(map) {
    const m = {};

    const getDirection = (start, end) => {
      const dx = end[0] > start[0] ? 1 : -1;
      const dy = end[1] > start[1] ? 1 : -1;

      const q = [[start[0], start[1], ""]];
      const paths = [];

      while (q.length > 0) {
        const [x, y, path] = q.shift();
        if (map[y][x] === "*") continue;
        if (x === end[0] && y === end[1]) {
          paths.push(path + "A");
          continue;
        }
        for (let dir of [
          [0, dy],
          [dx, 0],
        ]) {
          const newX = x + dir[0];
          const newY = y + dir[1];
          if (
            newX < 0 ||
            newX >= map[0].length ||
            newY < 0 ||
            newY >= map.length
          )
            continue;

          const char = dir[0] != 0 ? (dx > 0 ? ">" : "<") : dy > 0 ? "v" : "^";

          q.push([newX, newY, path + char]);
        }
      }
      return paths;
    };

    // Iterate through the grid
    for (let j = 0; j < map.length; j++) {
      for (let i = 0; i < map[0].length; i++) {
        if (map[j][i] === "*") continue;

        for (let y = 0; y < map.length; y++) {
          for (let x = 0; x < map[0].length; x++) {
            if (map[y][x] === "*") continue;

            const key = `${map[j][i]},${map[y][x]}`;
            m[key] = getDirection([i, j], [x, y]);
          }
        }
      }
    }
    return m;
  }

  getPaths(code, map) {
    let prev = "A";
    let paths = [""];

    for (let next of code) {
      const key = `${prev},${next}`;

      let temp = [];
      for (const path of paths) {
        for (let p of map[key]) temp.push(path + p);
      }
      paths = temp;
      prev = next;
    }

    return paths;
  }

  dfs(x, y, level, target, length) {
    const key = `${x},${y},${level}`;
    if (this.cache.has(key) && this.cache.get(key) < length)
      return this.cache.get(key);
    if (level >= target) return length;
    let l = 0;
    for (let path of this.dirMap[`${x},${y}`]) {
      // console.log("checking ", path, x, y, level, length);
      for (let i = 0; i < path.length - 1; i++) {
        l += this.dfs(
          path[i],
          path[i + 1],
          level + 1,
          target,
          length + path.length
        );
      }
    }
    this.cache.set(key, l);
    return l;
  }

  getShortest2(code) {
    let nested = 2;
    let paths = this.getPaths(code, this.numMap);
    console.log("Num", paths);

    // Arrow pad
    let l;
    let minL = Infinity;
    for (let p of paths) {
      l = 0;
      for (let i = 0; i < p.length - 1; i++) {
        // console.log(p[i], p[i + 1]);
        // console.log(this.dfs(p[i], p[i + 1], 0, 1, 0));
        l += this.dfs(p[i], p[i + 1], 0, 1, 0);
      }
      minL = Math.min(minL, l);
    }
    console.log("LEN", l, minL);
    return l;
  }

  getShortest(code) {
    let nested = 2;
    let paths = this.getPaths(code, this.numMap);
    console.log("Num", paths.length);

    // Arrow pad
    for (let i = 0; i < nested; i++) {
      let temp = [];
      for (let p of paths) {
        const newPaths = this.getPaths(p, this.dirMap);
        temp = temp.concat(newPaths);
      }
      paths = temp;
    }
    return paths.reduce((min, str) => Math.min(min, str.length), Infinity);
  }

  getCodes() {
    let ans = 0;
    for (let code of this.codes) {
      const pathLen = this.getShortest2(code);
      ans += parseInt(code.slice(0, 3)) * pathLen;
    }
    return ans;
  }
}

const runRAM = new RunRAM(true);
console.log("Day 21 part 1:", runRAM.getCodes());
// console.log("Day 20 part 2:", runRAM.getByte());


//     +---+---+
//     | ^ | A |
// +---+---+---+
// | < | v | > |
// +---+---+---+

// +---+---+---+
// | 7 | 8 | 9 |
// +---+---+---+
// | 4 | 5 | 6 |
// +---+---+---+
// | 1 | 2 | 3 |
// +---+---+---+
//     | 0 | A |
//     +---+---+
