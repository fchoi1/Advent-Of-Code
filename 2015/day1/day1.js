const fs = require("fs");

class Building {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.data = this.getInput();
    this.firstBasement = null;
  }

  getFloors() {
    let level = 0;
    const floors = this.data.split("");
    floors.forEach((bracket, i) => {
      if (bracket === "(") level++;
      else level--;
      if (level == -1 && !this.firstBasement) this.firstBasement = i + 1;
    });
    return level;
  }

  getFirstBasement() {
    return this.firstBasement;
  }
}

const building = new Building();
console.log("Day 1 part 1:", building.getFloors());
console.log("Day 1 part 2:", building.getFirstBasement());
