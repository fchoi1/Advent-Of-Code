const fs = require("fs");

class House {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return parseInt(fs.readFileSync(inputFile, "utf8").trim().split("\r\n")[0]);
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.target = this.getInput();
  }

  getlowestNumber(isPart2) {
    const multipler = isPart2 ? 11 : 10;
    let curr = 1;
    let currSum = 0;
    while (currSum < this.target ) {
      currSum = 0;
      for (let i = 1; i <= Math.ceil(Math.sqrt(curr)); i++) {
        if (curr % i === 0) {
          if (isPart2) {
            if (i * 50 > curr) currSum += multipler * i;
            if (i !== curr / i && (curr / i) * 50 > curr) currSum += (multipler * curr) / i;
          } else {
            currSum += multipler * i;
            if (i !== curr / i) currSum += (multipler * curr) / i;
          }
        }
      }
      curr += 1;
    }
    return curr - 1;
  }
}

const house = new House();
console.log("Day 20 part 1:", house.getlowestNumber());
console.log("Day 20 part 2:", house.getlowestNumber(true));
// Total Runtime ~1.9s
