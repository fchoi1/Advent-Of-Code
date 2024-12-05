const fs = require("fs");

class Report {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);

      const order = [];
      const render = [];
      let isOrder = true;
      data.forEach((line) => {
        if (!line) {
          isOrder = false;
          return;
        }
        if (isOrder) order.push(line.split("|").map((str) => parseInt(str)));
        else render.push(line.split(",").map((str) => parseInt(str)));
      });

      return [order, render];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.order, this.render] = this.getInput();
    this.nodeMap = this.getMap();
    this.incorrect = [];
    this.part1 = 0;
  }

  getMap() {
    const nodeMap = new Map();
    this.order.forEach(([a, b]) => {
      if (!nodeMap.has(a)) nodeMap.set(a, new Set());
      nodeMap.get(a).add(b);
    });
    return nodeMap;
  }

  isCorrectOrder(line) {
    const seen = new Set();
    for (let node of line) {
      const intersection = new Set(
        [...(this.nodeMap.get(node) || [])].filter((x) => seen.has(x))
      );
      if (intersection.size > 0) return false;

      seen.add(node);
    }
    return true;
  }

  processOrder() {
    this.render.forEach((line) => {
      if (!this.isCorrectOrder(line)) this.incorrect.push(line);
      else this.part1 += line[Math.floor(line.length / 2)];
    });
  }

  getCorrectOrder() {
    return this.part1;
  }

  getIncorrectOrder() {
    let middle = 0;
    for (let line of this.incorrect) {
      const lineSet = new Set(line);
      const order = [];

      while (lineSet.size > 0) {
        for (let node of lineSet) {
          const intersection = new Set(
            [...(this.nodeMap.get(node) || [])].filter((x) => lineSet.has(x))
          );
          if (intersection.size > 0) continue;
          order.push(node);
          lineSet.delete(node);
        }
      }
      middle += order[Math.floor(line.length / 2)];
    }
    return middle;
  }
}

const report = new Report();
report.processOrder();
console.log("Day 5 part 1:", report.getCorrectOrder());
console.log("Day 5 part 2:", report.getIncorrectOrder());
