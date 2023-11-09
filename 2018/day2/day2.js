const fs = require("fs");

class Inventory {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.IDs = this.getInput();
    this.double = 0;
    this.triple = 0;
    this.processIDs();
  }

  processIDs() {
    this.idList = this.IDs.map((id) => {
      const count = Array(26).fill(0);
      for (const char of id) {
        count[char.charCodeAt(0) - "a".charCodeAt(0)]++;
      }
      if (count.some((n) => n == 2)) this.double++;
      if (count.some((n) => n == 3)) this.triple++;
      return count;
    });
  }

  isTarget(id1, id2) {
    if (id1.length !== id2.length) return false;
    let count = 0;
    let removeIndex;
    for (let i = 0; i < id1.length; i++) {
      if (id1[i] !== id2[i]) {
        removeIndex = i;
        count++;
      }
      if (count > 1) return { isTarget: false, index: null };
    }
    return { isTarget: true, index: removeIndex };
  }

  getChecksum() {
    return this.double * this.triple;
  }

  findCorrectID() {
    for (let i = 0; i < this.IDs.length; i++) {
      for (let j = i + 1; j < this.IDs.length; j++) {
        const result = this.isTarget(this.IDs[i], this.IDs[j]);
        if (result.isTarget) {
          return this.IDs[i].slice(0, result.index) + this.IDs[i].slice(result.index + 1);
        }
      }
    }
    return null;
  }
}

const inventory = new Inventory();
console.log("Day 2 part 1:", inventory.getChecksum());
console.log("Day 2 part 2:", inventory.findCorrectID());
