const fs = require("fs");

class Calibration {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((freq) => parseInt(freq));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.freq = this.getInput();
  }

  getFrequency() {
    return this.freq.reduce((prev, curr) => prev + curr, 0);
  }

  getFirstDupe() {
    const freqSet = new Set();
    let freq = 0;
    let index = 0;

    while (!freqSet.has(freq)) {
      freqSet.add(freq);
      freq += this.freq[index];
      index = (index + 1) % this.freq.length;
    }
    return freq;
  }
}

const calibration = new Calibration();
console.log("Day 1 part 1:", calibration.getFrequency());
console.log("Day 1 part 2:", calibration.getFirstDupe());
