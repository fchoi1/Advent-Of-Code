const fs = require("fs");

class MFCSAM {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = /Sue |: |, /;
    try {
      const aunts = [];
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      data.forEach((row) => {
        const [_, __, ...items] = row.split(delimiters);
        const gift = {};
        items.forEach((item, i) => {
          if (i % 2 === 0) gift[item] = parseInt(items[i + 1]);
        });
        aunts.push(gift);
      });
      return aunts;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.aunts = this.getInput();
    this.searchObj = {
      children: 3,
      cats: 7,
      samoyeds: 2,
      pomeranians: 3,
      akitas: 0,
      vizslas: 0,
      goldfish: 5,
      trees: 3,
      cars: 2,
      perfumes: 1,
    };
  }

  getSue() {
    const possibleAunt = [];
    this.aunts.forEach((aunt, i) => {
      const isPossible = Object.entries(this.searchObj).every(([item, amount]) => {
        return !(item in aunt) || aunt[item] === amount;
      });
      if (isPossible) possibleAunt.push(i);
    });
    return possibleAunt[0] + 1;
  }

  getNewSue() {
    const possibleAunt = [];

    this.aunts.forEach((aunt, i) => {
      const isPossible = Object.entries(this.searchObj).every(([item, amount]) => {
        if (item in aunt) {
          if (["trees", "cats"].includes(item)) {
            return aunt[item] > amount;
          } else if (["pomeranians", "goldfish"].includes(item)) {
            return aunt[item] < amount;
          } else {
            return aunt[item] === amount;
          }
        } else {
          return true;
        }
      });

      if (isPossible) possibleAunt.push(i);
    });
    return possibleAunt[0] + 1;
  }
}

const mfcsam = new MFCSAM();
console.log("Day 16 part 1:", mfcsam.getSue());
console.log("Day 16 part 2:", mfcsam.getNewSue());
