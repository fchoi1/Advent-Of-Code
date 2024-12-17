const fs = require("fs");
const { run } = require("node:test");

class Warehouse {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      const register = {};
      let program;
      data.forEach((row) => {
        if (!row) return;
        const split = row.split(" ");
        if (split[0] === "Register") {
          const r = split[1].split(":")[0];
          register[r] = parseInt(split[2]);
        } else {
          program = split[1].split(",").map(Number);
        }
      });
      return [program, register];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.reset();
    this.opcodes = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"];
  }

  reset() {
    [this.program, this.register] = this.getInput();
    this.index = 0;
    this.out = [];
  }

  getComboOp(op) {
    if (op <= 3) return op;
    if (op === 4) return this.register.A;
    if (op === 5) return this.register.B;
    if (op === 6) return this.register.C;
    return null;
  }

  applyOp(op, x) {
    if (op === "adv") {
      this.register.A = Math.floor(this.register.A / 2 ** this.getComboOp(x));
    } else if (op === "bxl") {
      this.register.B ^= x;
    } else if (op === "bst") {
      this.register.B = this.getComboOp(x) % 8;
    } else if (op === "jnz") {
      if (this.register.A === 0) return false;
      this.index = x;
      return true;
    } else if (op === "bxc") {
      this.register.B ^= this.register.C;
    } else if (op === "out") {
      this.out.push(this.getComboOp(x) % 8);
    } else if (op === "bdv") {
      this.register.B = Math.floor(this.register.A / 2 ** this.getComboOp(x));
    } else if (op === "cdv") {
      this.register.C = Math.floor(this.register.A / 2 ** this.getComboOp(x));
    }
    return false;
  }

  runProgram(target = null) {
    let ans = 0;

    // this.register.C = 9;
    // this.applyOp("bst", 6);
    // console.log(this.register.B);

    // this.register.A =10;
    // this.applyOp("bst", 6);
    // console.log(this.register.B);

    while (this.index < this.program.length) {
      const op = this.opcodes[this.program[this.index]];
      const x = this.program[this.index + 1];
      const hasJumped = this.applyOp(op, x);
      if (!hasJumped) this.index += 2;

      // if (target && this.out.length > target.length) return this.out.join(",");
    }
    return this.out.join(",");
  }

  testA(A) {
    this.reset();
    this.register.A = A;
    return this.runProgram(this.program);
  }

  getA() {
    let A = 0;
    const target = this.program.join(",");
    let out = "";
    let curr = 0;
    console.log(
      this.program.length,
      "digits",
      String(8 ** 16),
      String(8 ** 16).length
    );

    // Digits increase by 8

    // while (target !== out && A < 1000) {
    //   // if (A % 100 === 0) console.log(A);
    //   // console.log(out)
    //   A += 1;
    //   this.reset();
    //   this.register.A = A;
    //   out = this.runProgram(this.program);
    //   // if (out.length != curr) console.log(A);

    //   const num = out.split(",").join("");
    //   console.log(A, num);
    //   if (num == "530") {
    //     // console.log("530:", A, A * 8);
    //     // digits.push(A * 8);
    //   }
    //   // console.log(num)
    //   curr = out.length;
    //   // if (A == 117440) console.log("REAL", out, "TARGET", target);
    // }

    let digits = [1];
    const t = [];

    // const test = [7, 5, 7, 2];
    // for (let i = test.length - 1; i >= 0; i--) {
    for (let i = this.program.length - 1; i >= 0; i--) {
      t.unshift(this.program[i]);
      const strT = t.join(",");
      console.log("Target", strT);
      let temp = [];
      while (digits.length > 0) {
        const d = digits.shift();
        for (let j = d - 64; j < d + 64; j++) {
          if (j < 0) continue;
          if (this.testA(j) === strT) {
            // console.log("Found", j, strT, this.testA(j));
            temp.push(j * 8);
          }
        }
      }
      digits = temp;
      // console.log("digits", digits);
    }
    console.log(
      this.testA(872155878029320 / 8),
      "::",
      this.program.join(","),
      this.testA(872155878029320 / 8) === this.program.join(",")
    );
    return Math.min(...digits) / 8;
  }
}

const warehouse = new Warehouse();
console.log("Day 15 part 1:", warehouse.getA());
// console.log("Day 15 part 2:", warehouse.getGPS());
// 109019476332289
