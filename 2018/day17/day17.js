const fs = require("fs");

class Reservoir {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => {
        const [first, n1, second, n2, n3] = row.split(/=|,|\.\./);
        const xCoord = first === "x" ? [parseInt(n1)] : [parseInt(n2), parseInt(n3)];
        const yCoord = first === "x" ? [parseInt(n2), parseInt(n3)] : [parseInt(n1)];
        return { x: xCoord, y: yCoord };
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.clays = this.getInput();
    this.walls = this.getWalls();
    this.stillWater = new Set();
    this.running = new Set();
    this.dropWater(500, 0, []);
  }

  printGrid() {
    console.log("\nGRID");
    for (let j = 0; j <= this.maxY + 1; j++) {
      let str = "";
      for (let i = this.minX; i < this.maxX; i++) {
        const key = `${i},${j}`;
        if (this.walls.has(key)) str += "#";
        else if (this.stillWater.has(key)) str += "~";
        else if (this.running.has(key)) str += "|";
        else str += ".";
      }
      console.log(str);
    }
  }

  getWalls() {
    const walls = new Set();
    let maxY = 0;
    let maxX = 0;
    let minX = Infinity;
    let minY = Infinity;
    this.clays.forEach(({ x, y }) => {
      const [start, end] = y.length > 1 ? y : x;
      for (let i = start; i <= end; i++) {
        const key = y.length > 1 ? `${x[0]},${i}` : `${i},${y[0]}`;
        walls.add(key);
      }
      maxY = Math.max(maxY, y[0], y[1] !== undefined ? y[1] : 0);
      minY = Math.min(minY, y[0], y[1] !== undefined ? y[1] : Infinity);
      maxX = Math.max(maxX, x[0], x[1] !== undefined ? x[1] : 0);
      minX = Math.min(minX, x[0], x[1] !== undefined ? x[1] : Infinity);
    });
    this.maxY = maxY;
    this.minY = minY;
    this.maxX = maxX + 1;
    this.minX = minX - 1;
    return walls;
  }

  dropWater(x, y, stack) {
    let key = `${x},${y}`;
    stack.push([x, y]);
    while (stack.length > 0) {
      while (y <= this.maxY && !this.stillWater.has(key) && !this.walls.has(key)) {
        if (y >= this.minY) {
          this.running.add(key);
          stack.push([x, y]);
        }
        y += 1;
        key = `${x},${y}`;
      }
      if (y > this.maxY) {
        [x, y] = stack.pop();
        key = `${x},${y}`;
        while (this.running.has(key)) {
          [x, y] = stack.pop();
          key = `${x},${y + 1}`;
          if (stack.length === 0) return;
        }
        continue;
      }

      const [floorX, floorY] = stack.pop();
      let floorSet = new Set([`${floorX},${floorY}`]);
      const [isRightStill, rCoords] = this.floorWater(floorX, floorY, 1, floorSet);
      const [isLeftStill, lCoords] = this.floorWater(floorX, floorY, -1, floorSet);
      if (isRightStill && isLeftStill) {
        floorSet.forEach((element) => {
          this.running.delete(element);
          this.stillWater.add(element);
        });
      } else floorSet.forEach((element) => this.running.add(element));
      if (rCoords) stack.push(rCoords);
      if (lCoords) stack.push(lCoords);
      if (stack.length === 0) return;
      [x, y] = stack.pop();
      key = `${x},${y}`;
    }
  }

  floorWater(x, y, direction, floorSet) {
    let key = `${x + direction},${y}`;
    while (!this.stillWater.has(key) && !this.walls.has(key)) {
      floorSet.add(key);
      if (!this.stillWater.has(`${x},${y + 1}`) && !this.walls.has(`${x},${y + 1}`)) return [false, [x, y]];
      x += direction;
      key = `${x},${y}`;
    }
    return [true, null];
  }

  getWaterCount() {
    return this.stillWater.size + this.running.size;
  }

  getStillWater() {
    return this.stillWater.size;
  }
}

const reservoir = new Reservoir();
console.log("Day 17 part 1:", reservoir.getWaterCount());
console.log("Day 17 part 2:", reservoir.getStillWater());
