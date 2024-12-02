const fs = require("fs");

class Historian {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      const list1 = [];
      const list2 = [];
      data.forEach((line) => {
        const [x, y] = line.split("  ").map((val) => parseInt(val));
        list1.push(x);
        list2.push(y);
      });
      return [list1, list2];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.list1, this.list2] = this.getInput();
    this.firstBasement = null;
  }

  getDiff() {
    const length = this.list1.length;
    const sorted1 = this.list1.sort((a, b) => a - b);
    const sorted2 = this.list2.sort((a, b) => a - b);
    let diff = 0;
    for (let i = 0; i < length; i++) {
      diff += Math.abs(sorted1[i] - sorted2[i]);
    }
    return diff;
  }
  getSimilarity() {
    const length = this.list1.length;
    const counts = {};
    for (let i = 0; i < length; i++) {
      if (!counts[this.list2[i]]) {
        counts[this.list2[i]] = 0;
      }
      counts[this.list2[i]]++;
    }

    let similarity = 0;
    for (let i = 0; i < length; i++) {
      similarity += this.list1[i] * counts[this.list1[i]] || 0;
    }
    return similarity;
  }
}

const historian = new Historian();
console.log("Day 1 part 1:", historian.getDiff());
console.log("Day 1 part 2:", historian.getSimilarity());
