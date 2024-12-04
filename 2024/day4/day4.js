const fs = require("fs");

class Search {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((dimension) => {
        return dimension.split("");
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.grid = this.getInput();
    this.w = this.grid[0].length;
    this.h = this.grid.length;
    this.target = "XMAS";
    this.dir = [
      [0, 1],
      [1, 0],
      [0, -1],
      [-1, 0],
      [1, 1],
      [-1, -1],
      [-1, 1],
      [1, -1],
    ];
  }

  isXmas(x, y, direction) {
    const [dx, dy] = direction;
    for (let k = 0; k < this.target.length; k++) {
      if (x < 0 || x >= this.w || y < 0 || y >= this.h) return false;
      if (this.grid[y][x] !== this.target[k]) return false;
      x += dx;
      y += dy;
    }

    return true;
  }

  countXmas() {
    let count = 0;

    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        for (let k = 0; k < this.dir.length; k++) {
          if (this.grid[j][i] === "X")
            count += this.isXmas(i, j, this.dir[k]) ? 1 : 0;
        }
      }
    }
    return count;
  }

  countX_mas() {
    let count = 0;
    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        if (this.grid[j][i] === "A") count += this.isX_mas(i, j) ? 1 : 0;
      }
    }
    return count;
  }

  isX_mas(x, y) {
    if (x - 1 >= 0 && y - 1 >= 0 && x + 1 < this.w && y + 1 < this.h) {
      return (
        (this.grid[y - 1][x - 1] === "M" &&
          this.grid[y - 1][x + 1] === "M" &&
          this.grid[y + 1][x + 1] === "S" &&
          this.grid[y + 1][x - 1] === "S") ||
        (this.grid[y - 1][x - 1] === "S" &&
          this.grid[y - 1][x + 1] === "S" &&
          this.grid[y + 1][x + 1] === "M" &&
          this.grid[y + 1][x - 1] === "M") ||
        (this.grid[y - 1][x - 1] === "M" &&
          this.grid[y + 1][x - 1] === "M" &&
          this.grid[y + 1][x + 1] === "S" &&
          this.grid[y - 1][x + 1] === "S") ||
        (this.grid[y - 1][x - 1] === "S" &&
          this.grid[y + 1][x - 1] === "S" &&
          this.grid[y + 1][x + 1] === "M" &&
          this.grid[y - 1][x + 1] === "M")
      );
    }
    return false;
  }
}

const search = new Search();
console.log("Day 4 part 1:", search.countXmas());
console.log("Day 4 part 2:", search.countX_mas());
