const fs = require("fs");

class Day2 {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((dimension) => {
        return dimension.split("x").map((str) => parseInt(str));
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.gifts = this.getInput();
  }

  getArea() {
    return 1;
  }
}

const day2 = new Day2();
console.log("Day 2 part 1:", day2.getArea());
// console.log("Day 2 part 2:", day2.getRibbonLength());
