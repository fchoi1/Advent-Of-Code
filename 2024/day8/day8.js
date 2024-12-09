const fs = require("fs");

class Guard {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((line) => {
        return line.split("");
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.grid = this.getInput();
    this.w = this.grid[0].length;
    this.h = this.grid.length;
    this.nodeMap = this.getNodeMap();
  }

  inRange(x, y) {
    return x >= 0 && x < this.w && y >= 0 && y < this.h;
  }

  getNodeMap() {
    const nodeMap = new Map();

    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        if (this.grid[j][i] === ".") continue;
        if (!nodeMap.has(this.grid[j][i])) nodeMap.set(this.grid[j][i], []);
        nodeMap.get(this.grid[j][i]).push(`${i},${j}`);
      }
    }
    return nodeMap;
  }

  countAntiNode(isPart2 = false) {
    const antiNode = new Set();
    for (const [_, neighbors] of this.nodeMap.entries()) {
      for (let i = 0; i < neighbors.length; i++) {
        const [x1, y1] = neighbors[i].split(",").map(Number);

        for (let j = i + 1; j < neighbors.length; j++) {
          const [x2, y2] = neighbors[j].split(",").map(Number);

          const dx = x2 - x1;
          const dy = y2 - y1;

          const p1 = { x: x2 + dx, y: y2 + dy };
          const p2 = { x: x1 - dx, y: y1 - dy };

          if (this.inRange(p1.x, p1.y)) antiNode.add(`${p1.x},${p1.y}`);
          if (this.inRange(p2.x, p2.y)) antiNode.add(`${p2.x},${p2.y}`);

          // Part 2 Only
          // Suprisingly, no need to reduce slope here :)
          if (!isPart2) continue;
          let addPointsInDirection = (x, y, dx, dy) => {
            while (this.inRange(x, y)) {
              antiNode.add(`${x},${y}`);
              x += dx;
              y += dy;
            }
          };
          addPointsInDirection(x1, y1, dx, dy);
          addPointsInDirection(x2, y2, -dx, -dy);
        }
      }
    }

    return antiNode.size;
  }
}

const guard = new Guard();
console.log("Day 8 part 1:", guard.countAntiNode());
console.log("Day 8 part 2:", guard.countAntiNode(true));
