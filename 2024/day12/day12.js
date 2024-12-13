const fs = require("fs");

class Pebbles {
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
    this.w = this.grid[0].length;
    this.h = this.grid.length;
    this.directions = [
      [1, 0], // right
      [0, 1], // down
      [-1, 0], //left
      [0, -1], // up
    ];
  }

  getPrice(x, y, seen, area, isPart2 = false) {
    let perimeter = 1;
    let region = new Set();

    const q = [{ x, y }];
    while (q.length > 0) {
      const { x, y } = q.shift();

      if (seen.has(`${x},${y}`)) {
        perimeter -= 1;
        continue;
      }
      perimeter += 3;

      seen.add(`${x},${y}`);
      region.add(`${x},${y}`);
      for (const [dx, dy] of this.directions) {
        const newX = x + dx;
        const newY = y + dy;

        if (newX < 0 || newX >= this.w || newY < 0 || newY >= this.h) continue;
        if (this.grid[newY][newX] !== area) continue;

        if (seen.has(`${newX},${newY}`)) {
          perimeter -= 1;
          continue;
        }
        q.push({ x: x + dx, y: y + dy });
      }
    }
    if (!isPart2) return perimeter * region.size;

    let edges = new Set();
    let isEdge = false;
    let start;

    for (const coord of region) {
      const [x, y] = coord.split(",").map(Number);
      for (const [dx, dy] of this.directions) {
        if (!region.has(`${x + dx},${y + dy}`)) {
          isEdge = true;
          break;
        }
      }
      if (isEdge) {
        edges.add(coord);
        if (
          !start &&
          !region.has(`${x - 1},${y}`) &&
          !region.has(`${x},${y - 1}`)
        )
          start = [x, y];
      }
    }

    let [currX, currY] = start;
    const seenEdges = new Set();
    let dir = 0;
    let startkey = `${x},${y},${this.directions[dir][0]},${this.directions[dir][1]}`;
    let key;
    let sides = 0;
    console.log("LETTER", area);
    // console.log("\n\nEdges", edges);
    let count = 0;
    while (startkey !== key) {
      count += 1;
      console.log("key", key, "start", startkey, area);

      const lx = this.directions[(dir + 4 - 1) % 4][0];
      const ly = this.directions[(dir + 4 - 1) % 4][1];
      while (
        edges.has(`${currX},${currY}`) &&
        !edges.has(`${currX + lx},${currY + ly}`)
      ) {
        seenEdges.add(`${currX},${currY}`);
        console.log("Adding", `${currX},${currY}`);
        currX += this.directions[dir][0];
        currY += this.directions[dir][1];
      }
      currX -= this.directions[dir][0];
      currY -= this.directions[dir][1];
      console.log("curr", currX, currY, this.directions[dir]);



      if (
        edges.has(`${currX + lx},${currY + ly}`) &&
        !seenEdges.has(`${currX + lx},${currY + ly}`)
      ) {
        dir = (dir + 4 - 1) % 4;
        console.log("TURN LEFT");
      } else {
        dir = (dir + 1) % 4;
        console.log("TURN RIGHT");
      }

      // if (
      //   edges.has(
      //     `${currX + this.directions[dir][0]},${
      //       currY + this.directions[dir][1]
      //     }`
      //   )
      // ) {
      //   currX += this.directions[dir][0];
      //   currY += this.directions[dir][1];
      // }

      sides += 1;
      key = `${currX},${currY},${this.directions[dir][0]},${this.directions[dir][1]}`;
      // console.log(dir, "New", currX, currY, sides);
      // console.log(key, seenEdges);
    }

    console.log(sides, perimeter, area);
    return sides * region.size;
  }

  countStones(isPart2 = false) {
    let cost = 0;
    const seen = new Set();
    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        const key = `${i},${j}`;
        if (seen.has(key)) continue;
        const c = this.getPrice(i, j, seen, this.grid[j][i], isPart2);

        cost += c;
      }
    }
    return cost;
  }
}

const pebbles = new Pebbles(true);
console.log("Day 12 part 1:", pebbles.countStones(true));
// console.log("Day 11 part 2:", pebbles.countStones(true));
