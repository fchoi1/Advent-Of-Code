const fs = require("fs");

class Tables {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const delimiters = / |,| -> /;
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data.map((circuit) => {
        const s = circuit.split(" -> ");
        return [s[0].split(" "), s[1]];
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.circuits = this.getInput();
    console.log(this.circuits);
    // 16 bits
  }

  getWires() {
    return;
  }
}

const tables = new Tables(true);
console.log("Day 7 part 1:", tables.getWires());
console.log("Day 7 part 2:");
// Total Runtime ~10.5
