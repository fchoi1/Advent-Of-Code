const fs = require("fs");

class Document {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";

    try {
      return fs.readFileSync(inputFile, "utf8").trim().split("\r\n")[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.json = this.getInput();
    this.delimiters = / |,|:|\[|\]|\{|\}/;
  }

  getSum(string) {
    return string.split(this.delimiters).reduce((sum, val) => (val && !isNaN(val) ? sum + parseInt(val) : sum), 0);
  }

  getStringSum() {
    return this.getSum(this.json);
  }

  getNonRedCount() {
    const splitted = this.json.replace(/([\[\]{}])/g, " $1 ").split(/\s+/);
    const stack = [];
    let currSum = 0;
    let hasRed = false;
    for (const currString of splitted) {
      if (!currString) continue;
      if ("{[".includes(currString)) {
        stack.push([currSum, hasRed]);
        currSum = 0;
      } else if ("]}".includes(currString)) {
        if (stack.length > 1) {
          let tempSum;
          [tempSum, hasRed] = stack.pop();
          currSum += tempSum;
        }
      } else {
        if (hasRed) continue;

        if (currString.includes(':"red')) {
          hasRed = true;
          currSum = 0;
        } else {
          currSum += this.getSum(currString);
        }
      }
    }
    return currSum;
  }
}

const document = new Document();
console.log("Day 11 part 1:", document.getStringSum());
console.log("Day 11 part 2:", document.getNonRedCount());
