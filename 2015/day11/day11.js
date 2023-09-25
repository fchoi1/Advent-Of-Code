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
    this.orderString = "abcdefghijklmnopqrstuvwxyz";
    this.invalidChar = "iol";
  }

  getCharPassword(password) {
    return [...password].reverse().map((char) => this.orderString.indexOf(char));
  }

  updatePassword() {
    let carryOver = 1;
    this.charPassword = this.charPassword.map((n, i) => {
      n += carryOver;
      carryOver = Math.floor(n / 26);
      return n % 26;
    });

    const stringPassword = this.charPassword
      .slice()
      .reverse()
      .reduce((pasword, n) => pasword + this.orderString[n], "");
    return stringPassword;
  }

  getNewPassword() {
    function reset() {
      hasSubtring = false;
      hasInvalid = false;
      doublePairs = [];
      prev = "";
      substring = "";
    }
    this.charPassword = this.getCharPassword(this.password);
    let prev;
    let substring;
    let stringPassword;
    let hasSubtring = false;
    let hasInvalid = false;
    let doublePairs = [];
    while (!hasSubtring || doublePairs.length < 2 || hasInvalid) {
      stringPassword = this.updatePassword();
      if (stringPassword === "zzzzzzzz") return "";
      reset();

      for (const char of stringPassword) {
        substring = stringPassword.slice(this.orderString.indexOf(char), this.orderString.indexOf(char) + 3);
        if (substring.length === 3 && this.orderString.includes(substring)) hasSubtring = true;
        if (this.invalidChar.includes(char)) {
          hasInvalid = true;
          break;
        }
        if (prev === char && !doublePairs.includes(char)) doublePairs.push(char);
        prev = char;
      }
    }
    this.password = stringPassword;
    return stringPassword;
  }
}

const password = new Password();
console.log("Day 11 part 1:", password.getNewPassword());
console.log("Day 11 part 2:", password.getNewPassword());
