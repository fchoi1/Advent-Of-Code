const fs = require("fs");

class Document {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const locationMap = {};
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split("\r\n")[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.password = this.getInput();
  }

  getSum() {
    return;
  }
}

const document = new Document();
console.log("Day 11 part 1:", document.getSum());
console.log("Day 11 part 2:");
