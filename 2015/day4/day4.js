const fs = require("fs");
const crypto = require("crypto");

class AdventCoins {
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
    this.key = this.getInput();
  }

  getHash(numZeros) {
    const target = "0".repeat(numZeros);
    let num = 0;
    let hash, keyStr, targetStr;
    while (targetStr !== target) {
      keyStr = this.key + String(num);
      hash = crypto.createHash("md5").update(keyStr).digest("hex");
      targetStr = hash.slice(0, target.length);
      num += 1;
    }
    return num - 1;
  }
}

const adventCoins = new AdventCoins();
console.log("Day 4 part 1:", adventCoins.getHash(5));
console.log("Day 4 part 2:", adventCoins.getHash(6));
// Total Runtime 16.2s
