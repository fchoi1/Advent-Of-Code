const fs = require("fs");

class Keypad {
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

  getNumMapPaths(code, map) {
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

  dfs(x, y, level, target) {
    const key = `${x},${y},${level}`;
    if (this.cache.has(key)) return this.cache.get(key);
    if (level >= target) return this.dirMap[`${x},${y}`][0].length;

    let minL = Infinity;
    for (let path of this.dirMap[`${x},${y}`]) {
      let l = 0;
      path = "A" + path;
      for (let i = 0; i < path.length - 1; i++) {
        l += this.dfs(path[i], path[i + 1], level + 1, target);
      }
      minL = Math.min(minL, l);
    }
    this.cache.set(key, minL);
    return minL;
  }

  getShortest(code, isPart2) {
    let loops = isPart2 ? 24 : 1;
    let paths = this.getNumMapPaths(code, this.numMap);
    let minL = Infinity;
    for (let p of paths) {
      let l = 0;
      p = "A" + p;
      for (let i = 0; i < p.length - 1; i++)
        l += this.dfs(p[i], p[i + 1], 0, loops);
      minL = Math.min(minL, l);
    }
    return minL;
  }

  getCodes(isPart2) {
    let ans = 0;
    this.cache = new Map();
    for (let code of this.codes)
      ans += parseInt(code.slice(0, 3)) * this.getShortest(code, isPart2);
    return ans;
  }
}

const keypad = new Keypad();
console.log("Day 21 part 1:", keypad.getCodes());
console.log("Day 21 part 2:", keypad.getCodes(true));
