const fs = require("fs");

class Sleigh {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((num) => parseInt(num));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.weights = this.getInput().reverse(); // Reverse to optimize 6x faster!
    this.sum = this.weights.reduce((sum, n) => sum + n, 0);
    this.reset();
  }

  reset(use4Groups = false) {
    const groups = use4Groups ? 4 : 3;
    this.groupSum = this.sum / groups;
    this.minLength = Infinity;
    this.qe = Infinity;
    this.seen = new Set();
  }

  calculateQE(numList) {
    return numList.reduce((product, n) => product * n, 1);
  }

  countCombinations(target, numList, remainingList) {
    if (numList.length > this.minLength || target > this.groupSum) return;

    numList.sort((a, b) => a - b);
    const key = numList.join(",");
    if (this.seen.has(key)) return;
    this.seen.add(key);

    if (target === this.groupSum) {
      if (numList.length < this.minLength) {
        this.qe = this.calculateQE(numList);
        this.minLength = numList.length;
      } else if (numList.length === this.minLength) {
        this.qe = Math.min(this.qe, this.calculateQE(numList));
      }
      return;
    }
    remainingList.forEach((n, i) => {
      const tempRemain = remainingList.slice();
      const tempNumList = numList.slice();
      tempRemain.splice(i, 1);
      tempNumList.push(n);
      this.countCombinations(target + n, tempNumList, tempRemain);
    });
  }

  getQE(use4Groups) {
    this.reset(use4Groups);
    this.countCombinations(0, [], this.weights);
    return this.qe;
  }
}

const sleigh = new Sleigh();
console.log("Day 24 part 1:", sleigh.getQE());
console.log("Day 24 part 2:", sleigh.getQE(true));
// Total Runtime ~2.8s
