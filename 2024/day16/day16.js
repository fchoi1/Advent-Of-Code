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
    let bestScore = Infinity;

    let count = 0;

    while (q.length > 0) {
      count += 1;

      q.sort((a, b) => {
        if (a[0] === b[0]) return a[4].size - b[4].size;
        return a[0] - b[0];
      });

      let [score, dir, start, prev, seen] = q.shift();
      const [x, y] = start;

      if (prev) {
        if (prevMap.has(`${prev[0]},${prev[1]}`)) {
          prevMap.set(
            `${x},${y}`,
            new Set([...seen, ...prevMap.get(`${prev[0]},${prev[1]}`)])
          );
        } else {
          prevMap.set(`${x},${y}`, new Set([...seen]));
        }
      }

      if (this.map[y][x] === "E") {
        console.log("\n\nFound end", score, seen.size);

        if (score < bestScore) {
          bestScore = score;
          prevMap.set(
            `${x},${y}`,
            new Set([...seen, ...prevMap.get(`${x},${y}`)])
          );
          visited.set(`${x},${y}`, [score, seen]);

          console.log(
            "new end",
            [x, y],
            this.end,
            prevMap.get(`${x},${y}`).size,
            visited.get(`${x},${y}`)[1].size,
            prevMap.get(`${prev[0]},${prev[1]}`).size
          );
          break;
        } else if (score === bestScore) {
          console.log("same score found", bestScore);

          prevMap.set(
            `${x},${y}`,
            new Set([...seen, ...prevMap.get(`${x},${y}`)])
          );
        } else {
          continue;
        }
      }

      const [dx, dy] = this.directions[dir];

      const key = `${x},${y}`;

      // const [dx, dy] = this.directions[dir];
      // const key = `${x},${y},${dx},${dy}`;
      if (visited.has(key)) {
        const [currScore, currSeen] = visited.get(key);
        if (score > currScore) continue;
        else {
          // console.log("seen prev", x, y, seen, currSeen);
          if (score == currScore) {
            // console.log(" ");
            console.log(
              "Same score",
              score,
              [x, y],
              prev,
              "seen",
              seen.size,
              "curr size",
              prevMap.get(`${x},${y}`).size,
              "prev size",
              prevMap.get(`${prev[0]},${prev[1]}`).size
            );
            // for (const item of q) {
            //   console.log(item[0], item[1], item[2], item[3], item[4].size);
            // }
            seen = new Set([...seen, ...currSeen]);
            visited.set(key, [score, new Set([...seen])]);
            prevMap.set(`${x},${y}`, new Set([...seen]));
            console.log("new prev", seen.size, prevMap.get(`${x},${y}`).size);

            // continue;
          } else {
            seen = new Set([...seen, ...currSeen]);
            visited.set(key, [score, new Set([...seen])]);
            prevMap.set(`${x},${y}`, new Set([...seen]));
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
    if (visited.has(`${this.end[0]},${this.end[1]},0,-1`))
      console.log(
        "top",
        visited.get(`${this.end[0]},${this.end[1]},0,-1`)[1].size
      );

    if (visited.has(`${this.end[0]},${this.end[1]},0,1`))
      console.log(
        "bottom",
        visited.get(`${this.end[0]},${this.end[1]},0,1`)[1].size
      );

    if (visited.has(`${this.end[0]},${this.end[1]},1,0`))
      console.log(
        "right",
        visited.get(`${this.end[0]},${this.end[1]},1,0`)[1].size
      );

    if (visited.has(`${this.end[0]},${this.end[1]},-1,0`))
      console.log(
        "left",
        visited.get(`${this.end[0]},${this.end[1]},-1,0`)[1].size
      );

    console.log(prevMap.get(`${this.end[0]},${this.end[1]}`).size);
    console.log(visited.get(`${this.end[0]},${this.end[1]}`).size);
    // this.printGrid(prevMap.get(`${this.end[0]},${this.end[1]}`), prevMap);

    // console.log(prevMap.get(`${this.end[0] - 1},${this.end[1]}`).size);
    // console.log(prevMap.get(`${this.end[0]},${this.end[1] + 1}`).size);

    return [bestScore];
  }

  printGrid(seen, prevMap) {
    for (let j = 0; j < this.map.length; j++) {
      let str = "";
      for (let i = 0; i < this.map[0].length; i++) {
        const key = `${i},${j}`;
        if (seen.has(key)) {
          str += "O";
        } else str += this.map[j][i];
      }
      console.log(str);
    }

    for (let j = 0; j < this.map.length; j++) {
      for (let i = 0; i < this.map[0].length; i++) {
        const key = `${i},${j}`;
        if (seen.has(key)) {
          if (prevMap.has(`${i},${j}`)) {
            console.log([i, j], "prev", prevMap.get(`${i},${j}`).size);
          }
        }
      }
    }
  }

  getGPS(isPart2 = false) {
    const [bestScore] = this.bfs();
    // console.log(paths);
    return bestScore;
  }
}

const warehouse = new Warehouse();
console.log("Day 15 part 1:", warehouse.getGPS());
// console.log("Day 15 part 1:", warehouse.getGPS());
