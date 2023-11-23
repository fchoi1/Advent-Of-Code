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
    console.log(this.maxY);
  }

  getWalls() {
    const walls = new Set();
    let maxY = 0;
    this.clays.forEach(({ x, y }) => {
      const [start, end] = y.length > 1 ? y : x;
      const range = Array.from({ length: end - start }, (_, index) =>
        y.length > 1 ? `${x[0]},${start + index}` : `${start + index},${y[0]}`
      );
      maxY = Math.max(maxY, y[0], y[1] !== undefined ? y[1] : 0);
      walls.add(...range);
    });
    this.maxY = maxY;
    return walls;
  }

  waterFalling(x, y, runningWater) {
    let key = `${x}, ${y}`;
    if (!this.stillWater.has(key) || this.walls.has(key)) return [x, y];
  }

  floorWater(x, y, direction, floorSet) {}

  dropWater(x, y, runningWater) {
    if (y > this.maxY) return [runningWater, [x, y]];
    let key = `${x}, ${y + 1}`;

    if (!this.stillWater.has(key) || this.walls.has(key)) {
      const [x, y] = this.waterFalling(x, y + 1, runningWater);
    }

    return [runningWater, [x, y]];

    return [runningWater, [x, y]];

    return [1, 1];
  }

  getWaterCount() {
    let flowWater = new Set();
    let prevSize;
    let pos = [500, 0];
    let loops = 0;
    while (loops < 100 && prevSize !== this.stillWater.size + flowWater.size) {
      const [running, coord] = this.dropWater(500, 0, new Set());
      loops++;
    }
    return 1;
  }
}

const reservoir = new Reservoir(true);
console.log("Day 17 part 1:", reservoir.getWaterCount());
