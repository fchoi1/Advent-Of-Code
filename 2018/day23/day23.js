const fs = require("fs");
const { init } = require("z3-solver");

class EET {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => {
        const [_, x, y, z, r] = row.split(/pos=<|,|>, r=/);
        return [x, y, z, r].map((n) => parseInt(n));
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.nanoBots = this.getInput();
    this.largest = this.getLargest();
    this.dim = this.findMaxMinValues();
    this.Xaxis = Infinity;
    this.Yaxis = Infinity;
    this.Zaxis = Infinity;
    this.Xlist = [];
    this.XlistMax = 0;
    this.XlistMin = Infinity;
    this.YlistMax = 0;
    this.YlistMin = Infinity;
    this.ZlistMax = 0;
    this.ZlistMin = Infinity;
  }

  findMaxMinValues() {
    return this.nanoBots.reduce(
      (acc, curr) => {
        acc.max = acc.max.map((max, index) => Math.max(max, curr[index]));
        acc.min = acc.min.map((min, index) => Math.min(min, curr[index]));
        return acc;
      },
      {
        max: Array.from({ length: 3 }, () => Number.MIN_SAFE_INTEGER),
        min: Array.from({ length: 3 }, () => 0),
      }
    );
  }

  getLargest() {
    return this.nanoBots.reduce((prev, curr) => (curr[3] > prev[3] ? curr : prev), this.nanoBots[0]);
  }

  getDistance(bot1, bot2) {
    return Math.abs(bot1[2] - bot2[2]) + Math.abs(bot1[1] - bot2[1]) + Math.abs(bot1[0] - bot2[0]);
  }

  getCountForLargest() {
    let count = 0;
    for (const bot of this.nanoBots) {
      if (this.getDistance(this.largest, bot) <= this.largest[3]) count++;
    }
    return count;
  }

  // Gave up and used z3 lib
  async getMostCount() {
    const { Context, em } = await init();
    const { Optimize, Int, If, LE, Sum } = new Context("main");
    const o = new Optimize();
    let x = Int.const("x");
    let y = Int.const("y");
    let z = Int.const("z");

    o.add(x.le(this.dim.max[0]));
    o.add(y.le(this.dim.max[1]));
    o.add(z.le(this.dim.max[2]));
    o.add(x.ge(this.dim.min[0]));
    o.add(y.ge(this.dim.min[1]));
    o.add(z.ge(this.dim.min[2]));

    for (const [p1, p2, p3, d] of this.nanoBots) {
      o.addSoft(
        LE(
          Sum(
            If(x.ge(p1), x.sub(p1), x.sub(p1).neg()),
            If(y.ge(p2), y.sub(p2), y.sub(p2).neg()),
            If(z.ge(p3), z.sub(p3), z.sub(p3).neg())
          ),
          d
        ),
        1
      );
    }
    await o.check();
    em.PThread.terminateAllThreads();
    return o.model().eval(Sum(x, y, z)).toString();
  }

  getCount(coord) {
    let count = 0;
    for (const bot of this.nanoBots) {
      if (this.getDistance(coord, bot) <= bot[3]) count++;
    }
    return count;
  }
}

const eet = new EET();
console.log("Day 23 part 1:", eet.getCountForLargest());
eet.getMostCount().then((result) => console.log("Day 23 part 2:", parseInt(result)));
// Runtime ~152.07s
