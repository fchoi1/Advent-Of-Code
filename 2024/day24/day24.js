const fs = require("fs");

class MonkeyMarket {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const startValues = new Map();
      const outputs = [];
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      let isOutputs = false;

      data.forEach((line) => {
        if (!line) {
          isOutputs = true;
          return;
        }
        if (!isOutputs) {
          const [name, value] = line.split(": ");
          startValues.set(name, parseInt(value));
        } else {
          const [a, cmd, b, _, out] = line.split(" ");
          outputs.push([a, b, cmd, out]);
        }
      });
      return [startValues, outputs];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.values, this.outputs] = this.getInput();
    this.ops = {
      AND: (a, b) => a & b,
      OR: (a, b) => a | b,
      XOR: (a, b) => a ^ b,
    };
    this.parseEdges();
    console.log(this.startValues, this.outputs);
    console.log("vars", this.vars);
  }

  parseEdges() {
    this.vars = new Map();
    for (const [a, b, cmd, out] of this.outputs) {
      this.vars.set(out, { a, b, cmd });
    }
  }

  calculateValue(node) {
    if (this.values.has(node)) {
      return this.values.get(node);
    }
    const { a, b, cmd } = this.vars.get(node);
    return this.ops[cmd](this.calculateValue(a), this.calculateValue(b));
  }

  getZ() {
    let ans = "";
    let key = "z00";
    while (this.vars.has(key)) {
      const val = this.calculateValue(key);
      ans = String(val) + ans;
      key = `z${(+key.slice(1) + 1).toString().padStart(2, "0")}`;
    }

    console.log(ans, ans.length);
    console.log("0011111101000".length)

    return parseInt(ans, 2);
  }


  // function to suppy inputs and get output
  // if we get a wrong answer proprate from output and check 
  // ex output was 0 but should be 1
  // a and b = 0
  // that means a must be 1 and b must be 1
  // other way arround is that a =1 ,b = 0, or b = 0, a = 1  or a = 0, b = 0
  // one of them is incorrct?
}

const monkeyMarket = new MonkeyMarket();
console.log("Day 24 part 1:", monkeyMarket.getZ());
