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
    this.cache = {};
    // console.log(this.values);
    // console.log("vars", this.vars);
  }

  makeKey(key, num) {
    return key + num.toString().padStart(2, "0");
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
    let num = 0;
    let key = this.makeKey("z", num);
    while (this.vars.has(key)) {
      ans = String(this.calculateValue(key)) + ans;
      num += 1;
      key = this.makeKey("z", num);
    }
    return ans;
  }

  getDecimal() {
    return parseInt(this.getZ(), 2);
  }

  printWire(wire, depth) {
    if (wire.startsWith("x") || wire.startsWith("y"))
      return `${" ".repeat(depth)}${wire}`;

    const { a, b, cmd } = this.vars.get(wire);
    const line = `${" ".repeat(depth)}${wire} ${cmd}\n${this.printWire(
      a,
      depth + 1
    )}\n${this.printWire(b, depth + 1)}`;
    return line;
  }

  validateProgram() {
    for (let i = 0; i < 45; i++) {
      if (!this.verify(i)) {
        console.log("Failed", i);
        return i;
      }
    }
    return 45;
  }

  part2() {
    console.log("\n\n");
    console.log(this.printWire("z02", 0));

    const swap = [];

    while (!this.validateProgram()) {}

    // check swaps

    // console.log(this.cache);

    // Swap
    // hbs <> kfp
    // dhq <> z18
    // z22 <> pdg
    // z27 <> jcp

    // const swap = ["hbs", "kfp", "dhq", "z18", "z22", "pdg", "z27", "jcp"];
    return swap.sort().join(",");
  }

  verifyImmeditate(key, num) {
    const { a, b, cmd } = this.vars.get(key);
    console.log("verifyImmeditate", key);

    if (cmd != "XOR") return false;

    const x = this.makeKey("x", num);
    const y = this.makeKey("y", num);
    return (a === x && b === y) || b === x || a === y;
  }

  verifyPrevCarry(key, num) {
    console.log("verifyPrevCarry", key);
    const { a, b, cmd } = this.vars.get(key);

    if (cmd != "AND") return false;
    const x = this.makeKey("x", num - 1);
    const y = this.makeKey("y", num - 1);
    return (a === x && b === y) || b === x || a === y;
  }

  verifyReCarry(key, num) {
    console.log("verifyReCarry", key);
    if (this.cache[key]) return true;

    const { a, b, cmd } = this.vars.get(key);
    if (cmd != "AND") return false;
    const valid =
      (this.verifyImmeditate(a, num - 1) && this.verifyCarry(b, num - 1)) ||
      (this.verifyImmeditate(b, num - 1) && this.verifyCarry(a, num - 1));

    if (valid) this.cache[key] = true;

    return valid;
  }

  verifyCarry(key, num) {
    console.log("verifyCarry", key);
    const { a, b, cmd } = this.vars.get(key);

    if (this.cache[key]) return true;

    if (cmd != "OR" && num !== 1) return false;

    const valid =
      num === 1
        ? this.verifyPrevCarry(key, num)
        : (this.verifyPrevCarry(a, num) && this.verifyReCarry(b, num)) ||
          (this.verifyPrevCarry(b, num) && this.verifyReCarry(a, num));

    if (valid) this.cache[key] = true;

    return valid;
  }

  verify(num) {
    const key = this.makeKey("z", num);
    console.log("\nVerify", key);
    if (key === "z00") return this.verifyImmeditate(key, 0);

    const { a, b, cmd } = this.vars.get(key);
    if (cmd != "XOR") return false;

    return (
      (this.verifyImmeditate(a, num) && this.verifyCarry(b, num)) ||
      (this.verifyImmeditate(b, num) && this.verifyCarry(a, num))
    );
  }

  // bit addition
  // First
  // carry = x and y
  // val = x xor y

  // Second
  // carry = (x and y) or (prev carry and (prev x xor  prev y))
  // val  = (x xor y) xor (prev carry and (prev x xor  prev y)) or (prev x and prev y))
  //      (either one)   xor  ( carry and only 1   or   both )
}

const monkeyMarket = new MonkeyMarket();
console.log("Day 24 part 1:", monkeyMarket.getDecimal());
console.log("Day 24 part 2:", monkeyMarket.part2());
