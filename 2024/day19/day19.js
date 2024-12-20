const fs = require("fs");

class RunRAM {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      let patterns;
      const designs = [];
      let curr = patterns;
      data.map((row) => {
        if (!row) {
          curr = designs;
          return;
        }
        if (curr === patterns) patterns = new Set(row.split(", "));
        else curr.push(row);
      });
      return [patterns, designs];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.patterns, this.designs] = this.getInput();
    this.getLongest();
    this.cache = new Map();
    console.log(this.longest, this.patterns.size, this.designs.length);
    this.filterPatterns();
    // console.log(this.cache);
    console.log(this.patterns.size, this.designs.length);
  }

  getLongest() {
    this.longest = 0;
    for (let p of this.patterns) {
      if (p.length > this.longest) this.longest = p.length;
    }
  }

  filterPatterns() {
    const unqiue = new Set();
    const list = [...this.patterns];
    for (let p of list) {
      this.patterns.delete(p);
      if (!this.bfs(p)) {
        this.cache.set(p, 1);
      } else {
        this.cache.set(p, this.bfs2(p) + 1);
      }
      this.patterns.add(p);
    }
    // this.patterns = unqiue;
  }

  bfs(string) {
    const q = [string];
    const seen = new Set();

    while (q.length > 0) {
      const str = q.shift();
      if (this.patterns.has(str)) return true;

      if (!str || str.length === 0) continue;
      if (seen.has(str)) continue;
      seen.add(str);

      for (let i = 0; i <= this.longest; i++) {
        if (this.patterns.has(str.slice(0, i))) {
          if (str.slice(i).length === 0) continue;
          q.push(str.slice(i));
        }
      }
    }
    return false;
  }

  bfs2(string) {
    const q = [string];
    const seen = new Set();
    let c = 0;

    while (q.length > 0) {
      // q.sort((a, b) => a.length - b.length);
      const str = q.shift();
      if (this.patterns.has(str)) {
        c += 1;
      }

      if (!str || str.length === 0) continue;
      if (seen.has(str)) continue;
      // seen.add(str);

      for (let i = 0; i <= this.longest; i++) {
        if (this.patterns.has(str.slice(0, i))) {
          if (str.slice(i).length === 0) continue;
          q.push(str.slice(i));
        }
      }
    }
    return c;
  }

  bfs3(string) {
    const q = [[string, 1]];
    const seen = new Set();
    let c = 0;

    while (q.length > 0) {
      // q.sort((a, b) => a.length - b.length);
      const [str, count] = q.shift();

      if (!str || str.length === 0) continue;
      if (seen.has(str)) continue;
      seen.add(str);

      if (this.patterns.has(str)) {
        // console.log("found a combo:", count, str);
        c += count;
      }

      for (let i = 0; i <= this.longest; i++) {
        if (this.patterns.has(str.slice(0, i))) {
          if (str.slice(i).length === 0) continue;
          // console.log(
          //   "found",
          //   str.slice(0, i),
          //   count * this.cache.get(str.slice(0, i))
          // );
          q.push([str.slice(i), count * this.cache.get(str.slice(0, i))]);
        }
      }
    }
    return c;
  }

  checkDesign(design) {
    // console.log(design);
    let c = 0;
    // console.log("design", design);
    if (this.cache.has(design)) {
      // console.log("cached", design, this.cache.get(design));
      return this.cache.get(design);
    }
    if (this.patterns.has(design)) {
      this.cache.set(design, 1);
      // console.log("seeting cache", design, 1, this.cache);
      c += 1;
    }

    for (let i = 0; i <= this.longest; i++) {
      if (this.patterns.has(design.slice(0, i))) {
        // console.log("Checking", design, "sliced", design.slice(i));
        if (design.slice(i).length === 0) continue;
        c += this.checkDesign(design.slice(i));
      }
    }
    if (c !== 0) {
      // console.log("set here c", design, c);
      this.cache.set(design, c);
    }
    // console.log("design", design, c);
    return c;
  }

  part1() {
    let ans = 0;
    // console.log(
    //   this.checkDesign(
    //     "brbbrrugubbbuwbrrwbwwggwrgbgbbbwrbbubbrggruggbgrgubgbbwgbubg"
    //   )
    // );
    for (let design of this.designs) {
      console.log(design);

      if (this.bfs(design)) {
        ans += 1;
      }
    }
    return ans;
  }

  part2() {
    let c = [];

    for (let design of this.designs) {
      // this.cache = new Map();
      console.log(design);
      const counts = this.bfs3(design);
      if (counts > 0) {
        // console.log("\n\ncount", counts, design);
        // console.log("\n\n");
        c.push(counts);
      }
    }
    console.log(c);
    return c.reduce((a, b) => a + b);
  }
}

const runRAM = new RunRAM();
// console.log("Day 19 part 1:", runRAM.part1());
console.log("Day 19 part 2:", runRAM.part2());
