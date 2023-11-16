const fs = require("fs");

class Plants {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    let initial = "";
    const havePlant = new Set();
    const noPlant = new Set();
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((item) => {
        if (item.includes("initial")) initial = item.split(" ")[2];
        if (item.includes("=>")) {
          item.split(" => ")[1] === "#" ? havePlant.add(item.split(" => ")[0]) : noPlant.add(item.split(" => ")[0]);
        }
      });
      return [initial, havePlant, noPlant];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.initial, this.havePlant, this.noPlant] = this.getInput();
  }

  calcSum(string, offset) {
    let total = 0;
    for (let i = 0; i < string.length; i++) {
      if (string[i] === "#") total += i - offset;
    }
    return total;
  }

  getSumofPots(isPart2) {
    const rounds = isPart2 ? 50_000_000_000 : 20;
    let currString = ".." + this.initial + "..";
    let offset = 2;
    let newString, prev, prevDiff, currRound;
    for (let r = 0; r < rounds; r++) {
      newString = "";
      for (let i = 2; i < currString.length; i++) {
        let checkStr = currString.slice(i - 3, i + 2);
        if (this.havePlant.has(checkStr)) newString += "#";
        else if (this.noPlant.has(checkStr)) newString += ".";
        else newString += this.useTest ? "." : currString[i];
      }
      offset += 2;
      currString = "..." + newString + "...";
      if (prevDiff === this.calcSum(currString, offset) - prev) {
        return (rounds - r - 1) * prevDiff + this.calcSum(currString, offset);
      }
      prevDiff = this.calcSum(currString, offset) - prev;
      prev = this.calcSum(currString, offset);
    }
    return this.calcSum(currString, offset);
  }
}

const plants = new Plants();
console.log("Day 12 part 1:", plants.getSumofPots());
console.log("Day 12 part 2:", plants.getSumofPots(true));
