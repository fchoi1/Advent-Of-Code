const fs = require("fs");

class FuelCell {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return parseInt(fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0]);
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.gridNum = this.getInput();
    this.gridSize = 300;
    this.grid = this.makePartialGrid();
  }

  makePartialGrid() {
    const grid = [Array(this.gridSize + 1).fill(0)];
    let currPower;
    for (let j = 1; j <= this.gridSize; j++) {
      const row = [0];
      currPower = 0;
      for (let i = 1; i <= this.gridSize; i++) {
        currPower += this.getPowerLevel(i, j);
        row.push(currPower + grid[j - 1][i]);
      }
      grid.push(row);
    }
    return grid;
  }

  getPowerLevel(x, y, grid) {
    const gridNum = grid ? grid : this.gridNum;
    const rackID = x + 10;
    const power = Math.floor(((rackID * y + gridNum) * rackID) / 100);
    return parseInt(String(power).slice(-1)) - 5;
  }

  getLargestCell(size) {
    let maxPower = -Infinity;
    let coords;
    for (let j = 0; j <= this.gridSize - size; j++) {
      for (let i = 0; i <= this.gridSize - size; i++) {
        let power = this.grid[j + size][i + size] - this.grid[j + size][i] - this.grid[j][i + size] + this.grid[j][i];
        if (power >= maxPower) {
          maxPower = power;
          coords = [i + 1, j + 1];
        }
      }
    }
    return [maxPower, coords];
  }

  getLargestPowerSize() {
    let largest = -Infinity;
    let largetCoords, largestSize;
    for (let size = 1; size <= this.gridSize; size++) {
      const [power, coords] = this.getLargestCell(size);
      if (power > largest) {
        largest = power;
        largetCoords = coords;
        largestSize = size;
      }
    }
    return [...largetCoords, largestSize].join(",");
  }
  getPower() {
    return this.getLargestCell(3)[1].join(",");
  }
}

const fuelCell = new FuelCell();
console.log("Day 11 part 1:", fuelCell.getPower());
console.log("Day 11 part 2:", fuelCell.getLargestPowerSize());
