const fs = require("fs");

class MonkeyMarket {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((x) => x.split("-"));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.connections = this.getInput();
    this.adjMap = this.getAdj();
    console.log(this.adjMap.size);
  }

  getAdj() {
    const adjMap = new Map();
    for (let [a, b] of this.connections) {
      if (!adjMap.has(a)) adjMap.set(a, new Set());
      if (!adjMap.has(b)) adjMap.set(b, new Set());
      adjMap.get(a).add(b);
      adjMap.get(b).add(a);
    }
    return adjMap;
  }

  findConnected(start, seen, paths) {
    let q = [[start, [start]]];

    while (q.length > 0) {
      const [node, path] = q.shift();

      if (path.length >= 3) {
        path.sort();
        if (this.adjMap.get(node).has(start)) paths.add(path.join(","));
        continue;
      }

      for (let next of this.adjMap.get(node)) {
        if (path.includes(next)) continue;
        q.push([next, [...path, next]]);
      }
    }

    seen.add(start);
    return paths;
  }

  getConnected() {
    const seen = new Set();
    const paths = new Set();

    for (let [node, _] of this.adjMap) {
      this.findConnected(node, seen, paths);
    }

    let ans = 0;
    for (let path of paths) {
      const computers = path.split(",");
      if (computers.some((c) => c.startsWith("t"))) ans += 1;
    }

    return ans;
  }

  dfs(node, seen) {
    if (seen.has(node)) {
      // check if longest, return, in this case we track along the path
      return;
    }
  }
}

// get largest loops, sounds like dfs is better!

const monkeyMarket = new MonkeyMarket();
console.log("Day 23 part 1:", monkeyMarket.getConnected());
