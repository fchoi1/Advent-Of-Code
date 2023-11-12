const fs = require("fs");

class Instructions {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const preReq = {};
    const dependantMap = {};
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((coords) => {
        const splitted = coords.split(" ");
        preReq[splitted[7]] = preReq[splitted[7]] || new Set();
        preReq[splitted[7]].add(splitted[1]);
        preReq[splitted[1]] = preReq[splitted[1]] || new Set();

        dependantMap[splitted[1]] = dependantMap[splitted[1]] || new Set();
        dependantMap[splitted[1]].add(splitted[7]);
        dependantMap[splitted[7]] = dependantMap[splitted[7]] || new Set();
      });
      return [preReq, dependantMap];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.reset();
  }

  reset() {
    [this.preReq, this.dependantMap] = this.getInput();
  }

  getOrder() {
    this.reset();
    let result = "";
    const nextList = Object.keys(this.preReq).filter((key) => this.preReq[key].size === 0);
    while (nextList.length !== 0) {
      nextList.sort((a, b) => b.localeCompare(a));
      const nextChar = nextList.pop();
      result += nextChar;
      this.updateDict(nextList, nextChar);
    }
    return result;
  }

  updateDict(nextList, nextChar) {
    this.dependantMap[nextChar].forEach((char) => {
      this.preReq[char].delete(nextChar);
      if (this.preReq[char].size === 0) {
        nextList.push(char);
      }
    });
  }

  getDuration() {
    this.reset();
    let result = "";
    const bonus = this.useTest ? 0 : 60;
    let workers = this.useTest
      ? [
          [-1, ""],
          [-1, ""],
        ]
      : [
          [-1, ""],
          [-1, ""],
          [-1, ""],
          [-1, ""],
          [-1, ""],
        ];
    const nextList = Object.keys(this.preReq).filter((key) => this.preReq[key].size === 0);
    let time = 0;
    while (nextList.length !== 0) {
      const temp = [];
      nextList.sort((a, b) => b.localeCompare(a));
      for (let i = 0; i < workers.length; i++) {
        const curr = workers[i];
        if (curr[0] === 0) {
          console.log("here")
          result += curr[1];
          this.updateDict(temp, nextChar);
          curr[1] = "";
        }
        if (curr[0] === -1 && nextList.length > 0) {
          const nextChar = nextList.pop();
          curr[1] = nextChar;
          curr[0] = nextChar.charCodeAt(0) - ("A".charCodeAt(0) - 1);
        }
        if (curr[0] >= 0) curr[0] -= 1;
      }
      nextList.push(...temp);
    }
    return result;
  }
}

const instructions = new Instructions(true);
console.log("Day 7 part 1:", instructions.getOrder());
console.log("Day 7 part 2:", instructions.getDuration());
