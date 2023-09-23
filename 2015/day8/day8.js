const fs = require("fs");

class Matchsticks {
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
    this.stringList = this.getInput();
    this.parseCharacter();
  }

  parseCharacter(getEncoded = false) {
    const encoded = this.stringList.reduce(
      (num, str) => {
        if (!str) return num + 2;
        let slash = 0;
        let slash2 = 0;
        let prev = "";
        let hex = 0;
        for (const char of str) {
          if (prev + char === "\\x") hex += 1;
          if (prev + char === "\\\\") {
            slash2 += 1;
            prev = "";
            continue;
          }
          if (char === "\\") slash += 1;
          if (char === '"') slash2 += 1;
          prev = char;
        }

        const part1 = num[0] + (slash + 2 + hex * 2);
        const part2 = num[1] + (slash + slash2 + 2);
        return [part1, part2];
      },
      [0, 0]
    );
    this.part1 = encoded[0];
    this.part2 = encoded[1];
  }

  getPart1() {
    return this.part1;
  }
  getPart2() {
    return this.part2;
  }
}

const matchsticks = new Matchsticks();
console.log("Day 8 part 1:", matchsticks.getPart1());
console.log("Day 8 part 2:", matchsticks.getPart2());
