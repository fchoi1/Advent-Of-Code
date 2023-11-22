const fs = require("fs");

class Classification {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const program = [];
    const opCodes = [];
    let opObj, values;
    let isOpCode = false;
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((row) => {
        if (!row) return;
        if (row.includes("Before")) {
          opObj = {};
          const splitted = row.split(/\[|]|, /).slice(1, 5);
          opObj.before = splitted.map((val) => parseInt(val));
          isOpCode = true;
        } else if (row.includes("After")) {
          const splitted = row.split(/\[|]|, /).slice(1, 5);
          opObj.after = splitted.map((val) => parseInt(val));
          opCodes.push(opObj);
          isOpCode = false;
        } else {
          values = row.split(" ").map((val) => parseInt(val));
          if (isOpCode) opObj.cmd = values;
          if (!isOpCode) program.push(values);
        }
      });
      return [program, opCodes];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.program, this.opCodes] = this.getInput();
    this.register = Array(4).fill(0);
    this.commands = this.getCommands();
    this.opCount = 0;
    this.codeMap = this.checkCodes();
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

  isEqual(register1, register2) {
    return register1.every((item, i) => item === register2[i]);
  }

  checkCodes() {
    let count = 0;
    const codeMapSet = Array(16).fill(new Set(Object.keys(this.commands)));
    this.opCodes.forEach(({ before, cmd, after }) => {
      let potential = [];
      const [num, a, b, c] = cmd;
      for (const key in this.commands) {
        const test = [...before];
        this.commands[key](a, b, c, test);
        if (this.isEqual(test, after)) potential.push(key);
      }
      if (potential.length >= 3) count++;
      codeMapSet[num] = new Set([...codeMapSet[num]].filter((x) => potential.includes(x)));
    });

    const codeMap = {};
    let toRemove = [];
    while (Object.keys(codeMap).length < 16) {
      const temp = [];
      Object.entries(codeMapSet).forEach(([key, codeSet]) => {
        if (codeSet.size === 1) {
          const val = [...codeSet][0];
          codeMap[key] = val;
          temp.push(val);
          codeSet.delete(key);
          return;
        }
        toRemove.forEach((item) => codeSet.delete(item));
      });
      toRemove = temp;
    }
    this.opCount = count;
    return codeMap;
  }

  getOpCount() {
    return this.opCount;
  }

  runProgram() {
    this.program.forEach(([cmd, a, b, c]) => {
      const cmdName = this.codeMap[cmd];
      this.commands[cmdName](a, b, c, this.register);
    });
    return this.register[0];
  }
}

const classification = new Classification();
console.log("Day 16 part 1:", classification.getOpCount());
console.log("Day 16 part 2:", classification.runProgram());
