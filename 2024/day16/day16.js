const fs = require("fs");

class Warehouse {
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
    // for (let row of this.map) {
    //   console.log(row.join(""));
    // }

    this.getLoc();
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
    console.log("analyzing");
    // score, dir, loc
    let q = [
      [0, 0, this.start, null, new Set([`${this.start[0]},${this.start[1]}`])],
    ];
    let visited = new Map();
    let prevMap = new Map();
    let paths = [];
    let bestScore = Infinity;

    while (q.length > 0) {
      // console.log(" ");
      // for (const item of q) {
      //   console.log(item[0], item[1], item[2], item[3], item[4].size);
      // }

      q.sort((a, b) => {
        if (a[0] === b[0]) return a[4].size - b[4].size;
        return a[0] - b[0];
      });

      let [score, dir, start, prev, seen] = q.shift();
      const [x, y] = start;

      if (prev) {
        prevMap.set(`${x},${y}`, seen);

        if (prevMap.has(`${prev[0]},${prev[1]}`)) {
          const prevSeen = prevMap.get(`${prev[0]},${prev[1]}`);
          seen = new Set([...seen, ...prevSeen]);
        }
      }

      if (this.map[y][x] === "E") {
        console.log("Found end", score, seen.size);
        if (score < bestScore) {
          bestScore = score;
          paths = [];
          paths.push(seen);
        } else if (score === bestScore) {
          paths.push(seen);
        } else {
          continue;
        }
      }

      const [dx, dy] = this.directions[dir];
      const key = `${x},${y},${dx},${dy}`;
      if (visited.has(key)) {
        const [currScore, currSeen] = visited.get(key);
        if (score > currScore) continue;
        else {
          // console.log("seen prev", x, y, seen, currSeen);
          if (score == currScore) {
            seen = new Set([...seen, ...currSeen]);
            visited.set(key, [score, seen]);
            continue;
          } else {
            seen = new Set([...seen, ...currSeen]);
            visited.set(key, [score, seen]);
          }
        }
      } else {
        visited.set(key, [score, seen]);
      }
      for (const [s, d] of [
        [1001, -1],
        [1, 0],
        [1001, 1],
      ]) {
        const [dx, dy] = this.directions[(dir + 4 + d) % 4];

        if (this.map[y + dy][x + dx] === "#") continue;
        const newD = (dir + 4 + d) % 4;

        const newSeen = new Set(seen);
        newSeen.add(`${x + dx},${y + dy}`);
        q.push([score + s, newD, [x + dx, y + dy], [x, y], newSeen]);
      }
    }

    console.log("seen", this.end);
    console.log(visited.get(`${this.end[0]},${this.end[1]},0,-1`)[1].size);
    console.log(prevMap.get(`${this.end[0]},${this.end[1]}`.size));
    // console.log(prevMap);
    // console.log(visited.get(`${this.end[0]},${this.end[1]},1,0`));
    // console.log(visited.get(`${this.end[0]},${this.end[1]},0,1`));
    // console.log(visited.get(`${this.end[0]},${this.end[1]},-1,0`));
    return [bestScore, paths];
  }

  getGPS(isPart2 = false) {
    const [bestScore, paths] = this.bfs();
    // console.log(paths);
    return bestScore;
  }
}

const warehouse = new Warehouse(true);
console.log("Day 15 part 1:", warehouse.getGPS());
