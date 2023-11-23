const fs = require("fs");

class Reservoir {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => {
        const [first, n1, second, n2, n3] = row.split(/=|,|\.\./);
        const xCoord = first === "x" ? [parseInt(n1)] : [parseInt(n2), parseInt(n3)];
        const yCoord = first === "x" ? [parseInt(n2), parseInt(n3)] : [parseInt(n1)];
        return { x: xCoord, y: yCoord };
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.clays = this.getInput();
  }
  getWaterCount() {
    return this.stillWater.size + this.running.size;
  }

  getStillWater() {
    return this.stillWater.size;
  }
}

const reservoir = new Reservoir();
console.log("Day 17 part 1:", reservoir.getWaterCount());
console.log("Day 17 part 2:", reservoir.getStillWater());
