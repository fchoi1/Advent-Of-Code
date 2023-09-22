const fs = require("fs");

class Strings {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.words = this.getInput();
  }
}

const strings = new Strings();
console.log("Day 6 part 1:");
console.log("Day 6 part 2:");
