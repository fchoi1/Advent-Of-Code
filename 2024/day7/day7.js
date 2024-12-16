const fs = require("fs");

class BridgeRepair {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((dimension) => {
        const split = dimension.split(": ");
        return {
          answer: parseInt(split[0]),
          numbers: split[1].split(" ").map((x) => parseInt(x)),
        };
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.equations = this.getInput();
  }

  isValid(ans, numbers, curr, index, isPart2 = false) {
    if (curr > ans) return false;
    if (index >= numbers.length) return ans === curr;
    const mul = this.isValid(
      ans,
      numbers,
      curr * numbers[index],
      index + 1,
      isPart2
    );
    const add = this.isValid(
      ans,
      numbers,
      curr + numbers[index],
      index + 1,
      isPart2
    );

    const concat = isPart2
      ? this.isValid(
          ans,
          numbers,
          parseInt(String(curr) + String(numbers[index])),
          index + 1,
          isPart2
        )
      : false;
    return mul || add || concat;
  }

  countValid(isPart2 = false) {
    let count = 0;
    this.equations.forEach(({ answer, numbers }) => {
      if (this.isValid(answer, numbers, numbers[0], 1, isPart2))
        count += answer;
    });
    return count;
  }
}

const bridgeRepair = new BridgeRepair();
console.log("Day 7 part 1:", bridgeRepair.countValid());
console.log("Day 7 part 2:", bridgeRepair.countValid(true));
