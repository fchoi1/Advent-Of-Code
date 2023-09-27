const fs = require("fs");

class Containers {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = /Sue |: |, /;
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data.map((row) => parseInt(row));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.containers = this.getInput();
    this.target = useTest ? 25 : 150;
    this.count = 0;
    this.duplicates = this.containers.filter((item, index) => this.containers.indexOf(item) !== index);
    this.minCount = 0;
    this.minLength = this.containers.length;
    this.countCombinations([], this.containers, new Set());
  }

  hasOnlyOneInstance(list, itemToCheck) {
    const filteredList = list.filter((item) => item === itemToCheck);
    return filteredList.length === 1;
  }

  calculateDuplicateCount(containerList) {
    return this.duplicates.reduce((duplicateCount, duplicate) => {
      return this.hasOnlyOneInstance(containerList, duplicate) ? duplicateCount * 2 : duplicateCount;
    }, 1);
  }

  getSum(containerList) {
    return containerList.reduce((sum, val) => val + sum, 0);
  }
  countCombinations(containerList, remainingConainers, visited) {
    containerList.sort();
    const key = containerList.join(",");

    if (visited.has(key)) return;
    visited.add(key);

    const currentSum = this.getSum(containerList);
    if (currentSum > this.target) return;
    if (currentSum === this.target) {
      const duplicateCount = this.calculateDuplicateCount(containerList);
      this.count += duplicateCount;

      if (containerList.length < this.minLength) {
        this.minLength = containerList.length;
        this.minCount = duplicateCount;
      } else if (containerList.length === this.minLength) {
        this.minCount += duplicateCount;
      }
      return;
    }
    remainingConainers.forEach((container, i) => {
      const newContainerlist = [...containerList];
      const newRemaining = [...remainingConainers];
      newContainerlist.push(container);
      newRemaining.splice(i, 1);
      this.countCombinations(newContainerlist, newRemaining, visited);
    });
  }

  getCombinations() {
    return this.count;
  }

  getMinLengthCombinations() {
    return this.minCount;
  }
}

const containers = new Containers();
console.log("Day 17 part 1:", containers.getCombinations());
console.log("Day 17 part 2:", containers.getMinLengthCombinations());
