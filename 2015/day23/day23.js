const fs = require("fs");

class Program {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const delimeters = / |\, \+|\, /;
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((item) => {
        let [command, register, jump] = item.split(delimeters);
        if (command === "jmp") {
          jump = null;
          register = parseInt(register);
        }
        return jump ? [command, register, parseInt(jump)] : [command, register];
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.instructions = this.getInput();
    this.register = { a: 0, b: 0 };
  }

  runProgram() {
    let index = 0;

    while (index >= 0 && index < this.instructions.length) {
      const [command, register, jump] = this.instructions[index];
      if (command === "jmp") {
        index += register;
        continue;
      }

      switch (command) {
        case "jmp":
          index += register;
          break;
        case "jio":
          index = this.register[register] === 1 ? index + jump : index + 1;
          break;
        case "jie":
          index = this.register[register] % 2 == 0 ? index + jump : index + 1;
          break;
        case "hlf":
          this.register[register] /= 2;
          break;
        case "tpl":
          this.register[register] *= 3;
          break;
        case "inc":
          this.register[register] += 1;
          break;
      }
      if (["hlf", "tpl", "inc"].includes(command)) index++;
    }
  }

  getRegisterB(isPart2) {
    this.register = isPart2 ? { a: 1, b: 0 } : { a: 0, b: 0 };
    this.runProgram();
    return this.register.b;
  }
}

const program = new Program();
console.log("Day 23 part 1:", program.getRegisterB());
console.log("Day 23 part 2:", program.getRegisterB(true));
