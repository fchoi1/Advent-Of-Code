const fs = require("fs");

class Mul {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split(/\r/)[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.program = this.getInput();
  }

  isInt(str) {
    const parsed = parseInt(str, 10);
    return !isNaN(parsed) && String(parsed) === str;
  }

  filterMul(str) {
    let newStr = "";
    let isDo = true;
    for (let i = 0; i < str.length; i++) {
      if (isDo) newStr += str[i];
      if (str.slice(i, i + 4) === "do()") isDo = true;
      else if (str.slice(i, i + 7) === "don't()") isDo = false;
    }
    return newStr;
  }

  getMul(isPart2 = false) {
    const programStr = isPart2 ? this.filterMul(this.program) : this.program;
    const open = /mul\(/;
    const split1 = programStr.split(open);

    const validPairs = [];
    split1.forEach((s) => {
      const string = s.split(")")[0];
      const strNum = string.split(",");
      if (strNum.length != 2) return;
      if (!this.isInt(strNum[0]) || !this.isInt(strNum[1])) return;
      validPairs.push([parseInt(strNum[0]), parseInt(strNum[1])]);
    });

    return validPairs.reduce((acc, curr) => acc + curr[0] * curr[1], 0);
  }
}

const mul = new Mul();
console.log("Day 3 part 1:", mul.getMul());
console.log("Day 3 part 2:", mul.getMul(true));
