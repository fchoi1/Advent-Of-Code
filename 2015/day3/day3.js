const fs = require("fs");

class Houses {
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
    this.directions = this.getInput();
    this.reset();
    this.dirMap = {
      ">": [1, 0],
      "<": [-1, 0],
      "^": [0, 1],
      v: [0, -1],
    };
  }

  reset() {
    this.santa = [0, 0];
    this.roboSanta = [0, 0];
    this.seen = new Set(["0,0"]);
  }

  getHousesWithPresents(useRobotSanta = false) {
    this.reset();
    this.directions.split("").forEach((direction, i) => {
      const [dx, dy] = this.dirMap[direction];
      let key;
      if (!useRobotSanta || (useRobotSanta && i % 2 == 0)) {
        this.santa = [this.santa[0] + dx, this.santa[1] + dy];
        key = `${this.santa[0]},${this.santa[1]}`;
      } else if (useRobotSanta && i % 2 == 1) {
        this.roboSanta = [this.roboSanta[0] + dx, this.roboSanta[1] + dy];
        key = `${this.roboSanta[0]},${this.roboSanta[1]}`;
      }

      this.seen.add(key);
    });
    return this.seen.size;
  }
}

const houses = new Houses();
console.log("Day 3 part 1:", houses.getHousesWithPresents());
console.log("Day 3 part 2:", houses.getHousesWithPresents(true));
