const fs = require("fs");

class Tables {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const circuits = {};
      const delimiters = / |,| -> /;
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      data.forEach((circuit) => {
        const s = circuit.split(" -> ");
        const val = s[0].split(" ");
        circuits[s[1]] = val.length === 1 ? val[0] : val;
      });
      return circuits;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.circuits = this.getInput();
    this.operator = {
      NOT: (operand1, operand2) => ~operand1 & 0xffff,
      OR: (operand1, operand2) => operand1 | operand2,
      AND: (operand1, operand2) => operand1 & operand2,
      XOR: (operand1, operand2) => operand1 ^ operand2,
      LSHIFT: (operand1, operand2) => (operand1 << operand2) & 0xffff,
      RSHIFT: (operand1, operand2) => operand1 >> operand2,
    };
  }

  getWire(wire) {
    if (this.wires[wire]) return this.wires[wire];
    const circuit = this.circuits[wire];

    if (!Array.isArray(circuit)) {
      const val = parseInt(circuit);
      this.wires[wire] = !isNaN(val) ? val : this.getWire(circuit);
      return this.wires[wire];
    }

    let command, val1, val2;
    if (circuit[0] === "NOT") {
      command = "NOT";
      val1 = circuit[1];
    } else {
      command = circuit[1];
      val1 = circuit[0];
      val2 = circuit[2];
    }

    const parseValue = (value) => {
      const val = parseInt(value);
      return !isNaN(val) ? val : this.getWire(value);
    };

    const evaluate = (operator, value1, value2 = null) => {
      return this.operator[operator](parseValue(value1), value2 === null ? null : parseValue(value2));
    };

    this.wires[wire] = command === "NOT" ? evaluate(command, val1) : evaluate(command, val1, val2);
    return this.wires[wire];
  }

  getWireA() {
    this.wires = {};
    return this.getWire("a");
  }

  getRewiredA() {
    this.wires = {};
    this.circuits["b"] = 46065;
    return this.getWire("a");
  }
}

const tables = new Tables();
console.log("Day 7 part 1:", tables.getWireA());
console.log("Day 7 part 2:", tables.getRewiredA());
