const fs = require("fs");

class Code {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const delimeters =
        /To continue, please consult the code grid in the manual.  Enter the code at row |, column |\./;
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0];
      return data
        .split(delimeters)
        .slice(1, 3)
        .map((n) => parseInt(n));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.row, this.col] = this.getInput();
    this.missing = [7, 1];
    this.latestPos = useTest ? this.getCodePosition(2, 6) : this.getCodePosition(6, 6);
    this.latestCode = useTest ? 4041754 : 27995004;
  }

  seriesSum(index, start) {
    return (index * (2 * start + (index - 1))) / 2;
  }

  getCodePosition(row, col) {
    const colSum = this.seriesSum(col, 1);
    const rowSum = this.seriesSum(row + col - 2, 1);
    const rowSubtract = this.seriesSum(col - 1, 1);
    return colSum + rowSum - rowSubtract;
  }

  getCode() {
    const targetCode = this.getCodePosition(this.row, this.col);
    let currPos = this.latestPos;
    let code = this.latestCode;

    while (currPos < targetCode) {
      code = (code * 252533) % 33554393;
      currPos++;
    }
    return code;
  }
}

const code = new Code();
console.log("Day 25 part 1:", code.getCode());
