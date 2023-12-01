const fs = require("fs");

class Constellations {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => row.split(",").map((n) => parseInt(n)));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.points = this.getInput();
  }

  getDist(pos1, pos2) {
    return pos1.reduce((dist, val, i) => dist + Math.abs(val - pos2[i]), 0);
  }

  findGroups(pos, seen) {
    const groupSet = [];
    for (const point of this.points) {
      const key = point.join(",");
      if (this.getDist(pos, point) <= 3 && !seen.has(key)) {
        groupSet.push(point);
        seen.add(key);
      }
    }
    groupSet.forEach((point) => this.findGroups(point, seen));
  }

  getGroups() {
    const seen = new Set();
    let count = 0;
    for (const point of this.points) {
      const key = point.join(",");
      if (seen.has(key)) continue;
      count++;
      this.findGroups(point, seen);
    }
    return count;
  }
}

const constellations = new Constellations();
console.log("Day 25 part 1:", constellations.getGroups());
