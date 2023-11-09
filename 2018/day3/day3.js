const fs = require("fs");

class Inventory {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = / @ |#|,|: |x/;
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((fabric) => {
        const values = fabric.split(delimiters).slice(2);
        return values.map((val) => parseInt(val));
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.fabrics = this.getInput();
    this.side = 1_000;
    this.fabricSet = new Set();
    this.duplicate = new Set();
    this.analyzeFabric();
  }

  analyzeFabric() {
    for (const [x, y, width, height] of this.fabrics) {
      for (let i = 0; i < width; i++) {
        for (let j = 0; j < height; j++) {
          if (this.fabricSet.has(`${x + i},${y + j}`)) {
            this.duplicate.add(`${x + i},${y + j}`);
          }
          this.fabricSet.add(`${x + i},${y + j}`);
        }
      }
    }
  }

  getOverlapped() {
    return this.duplicate.size;
  }

  getNonOverlapped() {
    for (const [index, [x, y, width, height]] of this.fabrics.entries()) {
      let overlapped = false;
      for (let i = 0; i < width; i++) {
        for (let j = 0; j < height; j++) {
          if (this.duplicate.has(`${x + i},${y + j}`)) {
            overlapped = true;
            break;
          }
        }
        if (overlapped) break;
      }
      if (!overlapped) return index + 1;
    }
    return -1;
  }
}

const inventory = new Inventory();
console.log("Day 3 part 1:", inventory.getOverlapped());
console.log("Day 3 part 2:", inventory.getNonOverlapped());
