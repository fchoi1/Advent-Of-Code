const fs = require("fs");

class Warehouse {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      const map = [];
      const commands = [];
      let curr = map;
      data.forEach((row) => {
        if (!row) {
          curr = commands;
          return;
        }
        curr.push(row.split(""));
      });
      return [map, commands.flat()];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.map, this.commands] = this.getInput();
    this.dir = {
      "<": [-1, 0],
      ">": [1, 0],
      "^": [0, -1],
      v: [0, 1],
    };
  }

  getStart(map) {
    for (let j = 0; j < map.length; j++) {
      for (let i = 0; i < map[0].length; i++) {
        if (map[j][i] === "@") return [i, j];
      }
    }
    return null;
  }

  getObstacles(map, isPart2 = false) {
    const obstacles = isPart2 ? new Map() : new Set();
    for (let j = 0; j < map.length; j++) {
      for (let i = 0; i < map[0].length; i++) {
        if (map[j][i] === "O") obstacles.add(`${i},${j}`);
        if (map[j][i] === "[") {
          obstacles.set(`${i},${j}`, true);
          obstacles.set(`${i + 1},${j}`, false);
        }
      }
    }
    return obstacles;
  }

  updateMap() {
    const newMap = [];
    for (let j = 0; j < this.map.length; j++) {
      const newRow = [];
      for (let i = 0; i < this.map[0].length; i++) {
        if (this.map[j][i] === "@") {
          newRow.push("@");
          newRow.push(".");
        } else if (this.map[j][i] === "O") {
          newRow.push("[");
          newRow.push("]");
        } else {
          newRow.push(this.map[j][i]);
          newRow.push(this.map[j][i]);
        }
      }
      newMap.push(newRow);
    }
    return newMap;
  }

  printGrid(map, pos, obstacles, isPart2 = false) {
    for (let j = 0; j < map.length; j++) {
      let str = "";
      for (let i = 0; i < map[0].length; i++) {
        if (pos[0] === i && pos[1] === j) str += "@";
        else if (!isPart2 && obstacles.has(`${i},${j}`)) str += "O";
        else if (isPart2 && obstacles.has(`${i},${j}`))
          str += obstacles.get(`${i},${j}`) ? "[" : "]";
        else if (map[j][i] === "#") str += "#";
        else str += ".";
      }
      console.log(str);
    }
  }

  canMove(map, obstacles, tempObs, curr, dir) {
    const [dx, dy] = dir;
    let [nextX, nextY] = curr;

    let key = `${nextX},${nextY}`;
    // Get the end of stack
    while (obstacles.has(key)) {
      obstacles.delete(key);
      tempObs.add(key);
      nextX += dx;
      nextY += dy;
      key = `${nextX},${nextY}`;
    }
    return map[nextY][nextX] !== "#";
  }

  canMove2(map, obs, tempObs, curr, dir) {
    const [dx, dy] = dir;
    if (map[curr[1]][curr[0]] === "#") return false;

    const key = `${curr[0]},${curr[1]}`;
    if (!obs.has(key)) return true;
    const l = obs.get(key) ? [curr[0], curr[1]] : [curr[0] - 1, curr[1]];
    const r = obs.get(key) ? [curr[0] + 1, curr[1]] : [curr[0], curr[1]];

    tempObs.set(`${l[0]},${l[1]}`, true);
    tempObs.set(`${r[0]},${r[1]}`, false);
    obs.delete(`${l[0]},${l[1]}`);
    obs.delete(`${r[0]},${r[1]}`);
    if (dx === -1)
      return this.canMove2(map, obs, tempObs, [l[0] + dx, l[1] + dy], dir);
    if (dx === 1)
      return this.canMove2(map, obs, tempObs, [r[0] + dx, r[1] + dy], dir);

    return (
      this.canMove2(map, obs, tempObs, [l[0] + dx, l[1] + dy], dir) &&
      this.canMove2(map, obs, tempObs, [r[0] + dx, r[1] + dy], dir)
    );
  }

  process2(isPart2 = false) {
    const map = isPart2 ? this.updateMap() : this.map;
    const obstacles = this.getObstacles(map, isPart2);
    const start = this.getStart(map);
    this.canMoveFn = isPart2 ? this.canMove2 : this.canMove;

    let curr = [start[0], start[1]];
    for (let c of this.commands) {
      const dx = this.dir[c][0];
      const dy = this.dir[c][1];
      const nextX = curr[0] + dx;
      const nextY = curr[1] + dy;

      const tempObs = isPart2 ? new Map() : new Set();

      const canMove = this.canMoveFn(
        map,
        obstacles,
        tempObs,
        [nextX, nextY],
        [dx, dy]
      );

      if (canMove) {
        for (const item of tempObs) {
          const nx =
            parseInt(isPart2 ? item[0].split(",")[0] : item.split(",")[0]) + dx;
          const ny =
            parseInt(isPart2 ? item[0].split(",")[1] : item.split(",")[1]) + dy;
          isPart2
            ? obstacles.set(`${nx},${ny}`, item[1])
            : obstacles.add(`${nx},${ny}`);
        }
        curr = [curr[0] + dx, curr[1] + dy];
      } else
        for (const item of tempObs) {
          isPart2 ? obstacles.set(item[0], item[1]) : obstacles.add(item);
        }
    }
    // this.printGrid(map, curr, obstacles, isPart2); // For debugging
    return obstacles;
  }

  getGPS(isPart2 = false) {
    let ans = 0;
    const obstacles = this.process2(isPart2);

    for (const coord of obstacles) {
      let x = 0;
      let y = 0;
      if (isPart2) {
        if (coord[1]) [x, y] = coord[0].split(",").map(Number);
      } else [x, y] = coord.split(",").map(Number);

      ans += x + y * 100;
    }
    return ans;
  }
}

const warehouse = new Warehouse();
console.log("Day 15 part 1:", warehouse.getGPS());
console.log("Day 15 part 2:", warehouse.getGPS(true));
