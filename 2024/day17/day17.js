const fs = require("fs");

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

  // combine
  // B = A % 8 ^ 5
  // C = A / 2 ** B
  // A /= 8

  // last 3 digits
  // 101 = 5
  //

  runProgram() {
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

    let digits = [1];
    const t = [];

    // const test = [7, 5, 7, 2];
    // for (let i = test.length - 1; i >= 0; i--) {
    for (let i = this.program.length - 1; i >= 0; i--) {
      t.unshift(this.program[i]);
      const strT = t.join(",");
      let temp = [];
      console.log(strT);
      while (digits.length > 0) {
        const d = digits.shift();
        for (let j = d; j < d + 8; j++) {
          if (this.testA(j) === strT) {
            console.log("found", j, String(j).length);
            temp.push(j * 8);
          }
          if (temp.length > 8) break;
        }
      }
      digits = temp;
    }
    console.log("done:", digits);
    const ans = Math.min(...digits) / 8;
    console.log(
      this.testA(ans),
      "::",
      this.program.join(","),
      this.testA(ans) === this.program.join(",")
    );

    console.log(String(Math.min(...digits) / 8).length);
    return Math.min(...digits) / 8;
  }

  // 2,4, bst -> 4  B = A % 8
  // 1,5, bxl -> 5  B ^= 5
  // 7,5, cdv -> 5  C = A /  2 ** b
  // 0,3, adv -> 3  A  =  A / 8
  // 4,0, bxc -> 0  B ^= C
  // 1,6, bxl -> 6  B ^= 6
  // 5,5, out -> 5  B % 8
  // 3,0  jnz -> jump to 0

  find(program, ans) {
    let sub = null;
    if (program.length === 0) return ans;
    const end = program.length - 1;
    for (let i = 0; i < 8; i++) {
      const a = ans * 8 + i;
      let b = a % 8;
      b ^= 5;
      let c = Math.floor(a / 2 ** b);
      b ^= c;
      b ^= 6;
      if (b % 8 === program[end]) {
        sub = this.find(program.slice(0, end), a);
        if (!sub) continue;
        return sub;
      }
    }
    return null;
  }

  // find(program, ans) {
  //   // console.log(program, ans);
  //   let sub = null;
  //   if (program.length === 0) return ans;
  //   const end = program.length - 1;
  //   for (let i = 0; i <= 8; i++) {
  //     const a = ans * 8 + i;
  //     let b = a % 8;
  //     b ^= 2;
  //     let c = Math.floor(a / 2 ** b);
  //     b ^= c;
  //     b ^= 3;
  //     if (b % 8 === program[end]) {
  //       sub = this.find(program.slice(0, end), a);
  //       if (!sub) continue;
  //       return sub;
  //     }
  //   }
  //   return sub;
  // }

  part2() {
    return this.find(this.program, 0);
  }
}

const warehouse = new Warehouse();
console.log("Day 15 part 1:", warehouse.runProgram());
console.log("Day 15 part 2:", warehouse.getA());
console.log("Day 15 part 2a:", warehouse.part2());
// console.log("Day 15 part 2:", warehouse.getGPS());
// 109019476332289
// 109019476330651
