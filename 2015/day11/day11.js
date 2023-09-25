const fs = require("fs");

class Password {
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

  getNewPassword() {
    return;
  }
}

const password = new Password();
console.log("Day 11 part 1:", password.getNewPassword());
console.log("Day 11 part 2:");
// Total Runtime ~13s
