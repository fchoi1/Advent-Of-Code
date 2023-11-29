const fs = require("fs");

class OpCode {
  getInput() {
    const inputFile = this.useTest ? "input.txt" : "input.txt";
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
    this.firstHalt = null;
    this.lastHalt = null;
    this.runProgram();
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

  runProgram() {
    const minList = new Set();
    const register = Array(6).fill(0);
    const seen = new Set();
    while (register[this.ip] >= 0 && register[this.ip] < this.program.length) {
      const [cmd, a, b, c] = this.program[register[this.ip]];
      this.ops[cmd](a, b, c, register);
      const key = String(register[this.ip]) + "-" + register.join(",");
      if (seen.has(key)) break;
      seen.add(key);
      // Optimize Hardcode
      if (register[this.ip] === 18) {
        register[4] = Math.floor(register[3] / 256);
        register[5] = 1;
        register[this.ip] = 25;
      }
      if (register[this.ip] === 28) {
        if (!this.firstHalt) this.firstHalt = register[1];
        if (!minList.has(register[1])) {
          minList.add(register[1]);
          this.lastHalt = register[1];
        }
      }
      register[this.ip]++;
    }
  }
  getFirstHalt() {
    return this.firstHalt;
  }
  getLastHalt() {
    return this.lastHalt;
  }
}

const opCode = new OpCode();
console.log("Day 21 part 1:", opCode.getFirstHalt());
console.log("Day 21 part 2:", opCode.getLastHalt());
