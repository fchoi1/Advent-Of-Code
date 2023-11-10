const fs = require("fs");

class Alchemical {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.polymer = this.getInput();
  }

  isPolar(a, b) {
    if (a.toLowerCase() != b.toLowerCase()) return false;
    return (a.toLowerCase() === a && b.toUpperCase() === b) || (a.toUpperCase() === a && b.toLowerCase() === b);
  }

  getUnits(string) {
    let chemical = "";
    let prev = "";
    for (const char of string) {
      const isPolar = this.isPolar(prev, char);
      chemical = isPolar ? chemical.slice(0, -1) : chemical + char;
      prev = isPolar ? chemical.slice(-1) : char;
    }
    return chemical.length;
  }

  getShortestRemoved() {
    let minLength = Infinity;
    for (const char of "abcdefghijklmnopqrstuvwxyz") {
      const newPolymer = this.polymer.split(char).join("").split(char.toUpperCase()).join("");
      const units = this.getUnits(newPolymer);
      if (units < minLength) {
        minLength = units;
      }
    }
    return minLength;
  }

  getPolymerUnit() {
    return this.getUnits(this.polymer);
  }
}

const alchemical = new Alchemical();
console.log("Day 5 part 1:", alchemical.getPolymerUnit());
console.log("Day 5 part 1:", alchemical.getShortestRemoved());
