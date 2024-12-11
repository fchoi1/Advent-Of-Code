const fs = require("fs");

class Pebbles {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0];
      return data.split(" ").map(Number);
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.stones = this.getInput();
    this.cache = new Map();
  }

  getNextStone(s) {
    if (s === 0) return [1]; // length, s
    else if (String(s).length % 2 === 0) {
      const half = String(s).length / 2;
      return [
        parseInt(String(s).slice(0, half)),
        parseInt(String(s).slice(half)),
      ];
    } else return [2024 * s];
  }

  getCount(blinks, stone) {
    const nextS = this.getNextStone(stone);
    if (this.cache.has(`${blinks},${stone}`))
      return this.cache.get(`${blinks},${stone}`);

    if (blinks === this.target - 1) {
      this.cache.set(`${blinks},${stone}`, nextS.length);
      return nextS.length;
    }

    const len = nextS.reduce((acc, s) => acc + this.getCount(blinks + 1, s), 0);

    this.cache.set(`${blinks},${stone}`, len);
    return len;
  }

  countStones(isPart2 = false) {
    this.target = isPart2 ? 75 : 25;
    this.cache = new Map();
    return this.stones.reduce((acc, stone) => acc + this.getCount(0, stone), 0);
  }
}

const pebbles = new Pebbles();
console.log("Day 11 part 1:", pebbles.countStones());
console.log("Day 11 part 2:", pebbles.countStones(true));
