const fs = require("fs");

class LookAndSay {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const locationMap = {};
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split("\r\n")[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.input = this.getInput();
  }

  playRound(num) {
    const strList = String(num).split("");
    let strNum = "";
    let prev = strList[0];
    let count = 0;

    strList.forEach((char) => {
      if (char === prev) {
        count += 1;
      } else {
        strNum += count + prev;
        prev = char;
        count = 1;
      }
    });
    strNum += count + prev;
    return strNum;
  }

  getResult(rounds) {
    let i = 0;
    let val = this.input;
    while (i < rounds) {
      val = this.playRound(BigInt(val));
      i++;
    }
    return val.length;
  }
}

const lookAndSay = new LookAndSay();
console.log("Day 10 part 1:", lookAndSay.getResult(40));
console.log("Day 10 part 2:", lookAndSay.getResult(50));
// Total Runtime ~13s
