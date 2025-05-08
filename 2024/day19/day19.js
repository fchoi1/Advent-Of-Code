const fs = require("fs");

class RunRAM {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      let patterns;
      const designs = [];
      let curr = patterns;
      data.map((row) => {
        if (!row) {
          curr = designs;
          return;
        }
        if (curr === patterns) patterns = new Set(row.split(", "));
        else curr.push(row);
      });
      return [patterns, designs];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.patterns, this.designs] = this.getInput();
    this.longest = this.getLongest();
  }

  getLongest() {
    let longest = 0;
    for (let p of this.patterns) {
      if (p.length > longest) longest = p.length;
    }
    return longest;
  }

  bfs(string) {
    const q = [string];
    const seen = new Set();

    while (q.length > 0) {
      const str = q.shift();
      if (this.patterns.has(str)) return true;

      if (!str || str.length === 0) continue;
      if (seen.has(str)) continue;
      seen.add(str);

      for (let i = 0; i <= this.longest; i++) {
        if (this.patterns.has(str.slice(0, i))) {
          if (str.slice(i).length === 0) continue;
          q.push(str.slice(i));
        }
      }
    }
    return false;
  }

  countValidDesigns() {
    let ans = 0;
    for (let design of this.designs) {
      if (this.bfs(design)) ans += 1;
    }
    return ans;
  }

  subtractSuffix(str1, str2) {
    return str1.endsWith(str2) ? str1.slice(0, -str2.length) : str1;
  }

  getCounts(design) {
    let dp = new Map(); // string: count
    let s = "";

    for (let i = 0; i < design.length; i++) {
      let currCount = 0;
      s += design[i];

      let subString = "";
      for (let j = i; j >= 0; j--) {
        subString = design[j] + subString;
        if (subString.length > this.longest) break;

        if (this.patterns.has(subString)) {
          const subtracted = this.subtractSuffix(s, subString);
          if (subtracted === "") currCount += 1;
          else currCount += dp.get(subtracted, 0);
        }
      }
      dp.set(s, currCount);
    }
    return dp.get(design);
  }

  getAllCombos() {
    let total = 0;
    for (let design of this.designs) {
      total += this.getCounts(design);
    }
    return total;
  }
}

const runRAM = new RunRAM();
console.log("Day 19 part 1:", runRAM.countValidDesigns());
console.log("Day 19 part 2:", runRAM.getAllCombos());
