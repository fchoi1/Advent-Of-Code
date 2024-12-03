const fs = require("fs");

class Report {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((dimension) => {
        return dimension.split(" ").map((str) => parseInt(str));
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.reports = this.getInput();
  }

  isValid(report) {
    let prev;
    const inc = report[1] > report[0];
    for (let val of report) {
      if (!prev) {
        prev = val;
        continue;
      }

      const isUnsafe =
        Math.abs(val - prev) > 3 ||
        val == prev ||
        (inc && val < prev) ||
        (!inc && val > prev);

      if (isUnsafe) return false;
      prev = val;
    }
    return true;
  }

  isValid2(report) {
    for (let i = 0; i < report.length; i++) {
      const removed = report.splice(i, 1);

      if (this.isValid(report)) return true;
      report.splice(i, 0, ...removed);
    }
  }

  getArea(isPart2 = false) {
    let count = 0;
    this.reports.forEach((report) => {
      if (isPart2 && (this.isValid(report) || this.isValid2(report))) count++;
      else if (this.isValid(report)) count++;
    });

    return count;
  }
}

const report = new Report();
console.log("Day 2 part 1:", report.getArea());
console.log("Day 2 part 2:", report.getArea(true));
