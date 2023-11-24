const fs = require("fs");

class OpCode {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      let ip;
      const commands = [];
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((row) => {
        if (row.includes("#ip")) return (ip = parseInt(row.split(" ")[1]));
        const [cmd, n1, n2, n3] = row.split(" ");
        commands.push([cmd, parseInt(n1), parseInt(n2), parseInt(n3)]);
      });
      return [commands, ip];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.program, this.ip] = this.getInput();
    this.ops = this.getCommands();
  }

  getCommands() {
    return {
      addr: (a, b, c, register) => (register[c] = register[a] + register[b]),
      addi: (a, b, c, register) => (register[c] = register[a] + b),
      mulr: (a, b, c, register) => (register[c] = register[a] * register[b]),
      muli: (a, b, c, register) => (register[c] = register[a] * b),
      banr: (a, b, c, register) => (register[c] = register[a] & register[b]),
      bani: (a, b, c, register) => (register[c] = register[a] & b),
      boor: (a, b, c, register) => (register[c] = register[a] | register[b]),
      bori: (a, b, c, register) => (register[c] = register[a] | b),
      setr: (a, b, c, register) => (register[c] = register[a]),
      seti: (a, b, c, register) => (register[c] = a),
      gtir: (a, b, c, register) => (register[c] = +(a > register[b])),
      gtri: (a, b, c, register) => (register[c] = +(register[a] > b)),
      gtrr: (a, b, c, register) => (register[c] = +(register[a] > register[b])),
      eqir: (a, b, c, register) => (register[c] = +(a === register[b])),
      eqri: (a, b, c, register) => (register[c] = +(register[a] === b)),
      eqrr: (a, b, c, register) => (register[c] = +(register[a] === register[b])),
    };
  }
  runProgram(isPart2) {
    this.register = Array(6).fill(0);
    if (isPart2) this.register[0] = 1;
    while (this.register[this.ip] >= 0 && this.register[this.ip] < this.program.length) {
      const [cmd, a, b, c] = this.program[this.register[this.ip]];
      this.ops[cmd](a, b, c, this.register);
      // Hardcode Optimize
      if (this.register[this.ip] === 3) {
        this.register[3] = this.register[1] + 1;
        if (this.register[1] % this.register[5] === 0) this.register[0] += this.register[5];
        this.register[this.ip] = 11;
      }
      this.register[this.ip]++;
    }
    return this.register[0];
  }
}

const opCode = new OpCode();
console.log("Day 19 part 1:", opCode.runProgram());
console.log("Day 19 part 2:", opCode.runProgram(true));
// Total Runtime ~1.28s
