const fs = require("fs");

class Strings {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.words = this.getInput();
  }

  isNice2(word) {
    const doublePairSet = new Set();
    let str3 = "";
    let prevDouble = "";
    let hasInBetween = false;
    let hasDoublePair = false;

    for (const char of word.split("")) {
      if (str3.length == 3) {
        str3 = str3.slice(1);
      }
      str3 += char;
      if (str3.charAt(0) === str3.charAt(2)) hasInBetween = true;

      const temp = prevDouble;

      if (prevDouble.length == 2) {
        doublePairSet.add(prevDouble);
        prevDouble = prevDouble.slice(1);
      }
      prevDouble += char;

      if (temp == prevDouble) prevDouble = prevDouble.slice(1);
      if (doublePairSet.has(prevDouble)) hasDoublePair = true;
      if (hasInBetween && hasDoublePair) return true;
    }
    return false;
  }

  isNice(word) {
    let prev;
    let vowels = [];
    let repeatChars = false;
    let hasErrorChar = false;
    for (const char of word.split("")) {
      if (prev === char) repeatChars = true;
      if ("aeiou".includes(char)) vowels.push(char);
      if (["ab", "cd", "pq", "xy"].includes(prev + char)) {
        hasErrorChar = true;
        break;
      }
      prev = char;
    }
    return !hasErrorChar && vowels.length >= 3 && repeatChars;
  }

  getNice(useNice2 = false) {
    return this.words.filter(useNice2 ? this.isNice2 : this.isNice).length;
  }
}

const strings = new Strings();
console.log("Day 5 part 1:", strings.getNice());
console.log("Day 5 part 2:", strings.getNice(true));
