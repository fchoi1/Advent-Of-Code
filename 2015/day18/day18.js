const fs = require("fs");

class Lights {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data.map((row) => row.split(""));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.lightMap = this.getInput();
    this.steps = useTest ? 4 : 100;
    this.length = useTest ? 6 : 100;
    this.dirMap = [
      [0, 1],
      [0, -1],
      [1, 1],
      [1, -1],
      [1, 0],
      [-1, 0],
      [-1, 1],
      [-1, -1],
    ];
    this.alwaysOn = [
      [0, 0],
      [this.length - 1, 0],
      [0, this.length - 1],
      [this.length - 1, this.length - 1],
    ];
  }

  isInBounds(position) {
    const [x, y] = position;
    return x >= 0 && x < this.length && y >= 0 && y < this.length;
  }

  shouldBeOn(position, keepCornersOn) {
    const [x, y] = position;
    const isCorner = this.alwaysOn.some(([coordX, coordY]) => coordX === x && coordY === y);
    if (keepCornersOn && isCorner) return true;
    const lightsOn = this.dirMap.reduce((count, [dx, dy]) => {
      return count + (this.isInBounds([x + dx, y + dy]) && this.lightMap[y + dy][x + dx] === "#");
    }, 0);
    return this.lightMap[y][x] === "#" ? [2, 3].includes(lightsOn) : lightsOn === 3;
  }

  updateLights(keepCornersOn) {
    this.lightMap = this.lightMap.map((row, j) =>
      row.map((_, i) => (this.shouldBeOn([i, j], keepCornersOn) ? "#" : "."))
    );
  }

  getLights(keepCornersOn) {
    this.lightMap = this.getInput();
    if (keepCornersOn) {
      for (const [x, y] of this.alwaysOn) {
        this.lightMap[y][x] = "#";
      }
    }

    for (let currStep = 0; currStep < this.steps; currStep++) {
      this.updateLights(keepCornersOn);
    }

    return this.lightMap.reduce((rowCount, row) => {
      const totalRowCount = row.reduce((lightCount, val) => (val === "#" ? ++lightCount : lightCount), 0);
      return totalRowCount + rowCount;
    }, 0);
  }
}

const lights = new Lights();
console.log("Day 18 part 1:", lights.getLights());
console.log("Day 18 part 2:", lights.getLights(true));
