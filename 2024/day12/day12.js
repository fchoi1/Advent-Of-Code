const fs = require("fs");

class GardenGroups {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => row.split(""));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.grid = this.getInput();
    this.part1 = 0;
    this.part2 = 0;
    this.w = this.grid[0].length;
    this.h = this.grid.length;
    this.directions = [
      [1, 0], // right
      [0, 1], // down
      [-1, 0], //left
      [0, -1], // up
    ];
    this.regions = this.getRegions();
  }

  processRegion(x, y, seen, area) {
    let perimeter = 1;
    let region = new Set();

    const q = [{ x, y }];
    while (q.length > 0) {
      const { x, y } = q.shift();

      if (seen.has(`${x},${y}`)) {
        perimeter -= 1;
        continue;
      }
      perimeter += 3;

      seen.add(`${x},${y}`);
      region.add(`${x},${y}`);
      for (const [dx, dy] of this.directions) {
        const newX = x + dx;
        const newY = y + dy;

        if (newX < 0 || newX >= this.w || newY < 0 || newY >= this.h) continue;
        if (this.grid[newY][newX] !== area) continue;

        if (seen.has(`${newX},${newY}`)) {
          perimeter -= 1;
          continue;
        }
        q.push({ x: x + dx, y: y + dy });
      }
    }
    return [perimeter * region.size, region];
  }

  getRegions() {
    let cost = 0;
    const regions = [];
    const seen = new Set();
    for (let j = 0; j < this.h; j++) {
      for (let i = 0; i < this.w; i++) {
        const key = `${i},${j}`;
        if (seen.has(key)) continue;
        const [c, r] = this.processRegion(i, j, seen, this.grid[j][i]);
        regions.push(r);
        cost += c;
      }
    }
    this.part1 = cost;
    return regions;
  }

  getSides(region) {
    let sides = 0;

    const hd = [
      [0.5, 0.5],
      [-0.5, 0.5],
      [-0.5, -0.5],
      [0.5, -0.5],
    ];

    const corners = new Set();
    for (const coord of region) {
      const [x, y] = coord.split(",").map(Number);
      hd.forEach(([dx, dy]) => corners.add(`${x + dx},${y + dy}`));
    }

    for (const coords of corners) {
      const [cx, cy] = coords.split(",").map(Number);
      const config = hd.map(([dx, dy]) => {
        return region.has(`${cx + dx},${cy + dy}`);
      });

      const s = config.reduce((acc, val) => acc + val, 0);
      if (s === 3 || s === 1) sides += 1;
      if (s === 2) {
        if ((config[0] && config[2]) || (config[1] && config[3])) sides += 2;
      }
    }

    return sides * region.size;
  }

  getPrice(isPart2 = false) {
    if (!isPart2) return this.part1;

    let cost = 0;
    for (const region of this.regions) {
      cost += this.getSides(region);
    }
    return cost;
  }
}

const gardenGroups = new GardenGroups();
console.log("Day 12 part 1:", gardenGroups.getPrice());
console.log("Day 12 part 2:", gardenGroups.getPrice(true));
