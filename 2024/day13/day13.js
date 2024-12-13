const fs = require("fs");

class ClawContraption {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      const prizes = [];
      let btnA, btnB, loc;
      data.forEach((row) => {
        if (!row) {
          prizes.push({ A: btnA, B: btnB, loc: loc });
          return;
        }
        const split = row.split(" ");
        if (split[0] === "Button") {
          const x = parseInt(split[2].split("+")[1]);
          const y = parseInt(split[3].split("+")[1]);
          if (split[1] === "A:") btnA = { x, y };
          else btnB = { x, y };
        } else {
          const x = parseInt(split[1].split("=")[1]);
          const y = parseInt(split[2].split("=")[1]);
          loc = { x, y };
        }
      });
      prizes.push({ A: btnA, B: btnB, loc: loc });
      return prizes;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.prizes = this.getInput();
    this.cost = { A: 3, B: 1 };
  }

  countStones(isPart2 = false) {
    let tokens = 0;

    for (const { A, B, loc } of this.prizes) {
      const locX = isPart2 ? loc.x + 10000000000000 : loc.x;
      const locY = isPart2 ? loc.y + 10000000000000 : loc.y;

      const bottom = B.x * A.y - B.y * A.x;
      const topB = locX * A.y - locY * A.x;
      const topA = locY * B.x - locX * B.y;

      const clickB = topB / bottom;
      const clickA = topA / bottom;

      if (Number.isInteger(clickA) && Number.isInteger(clickB)) {
        tokens += clickA * this.cost.A + clickB * this.cost.B;
      }
    }
    return String(tokens);
  }
}

const clawContraption = new ClawContraption();
console.log("Day 13 part 1:", clawContraption.countStones());
console.log("Day 13 part 2:", clawContraption.countStones(true));
