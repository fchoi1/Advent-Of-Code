const fs = require("fs");

class Code {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      const schemaList = [];
      let schema = [];
      data.forEach((line) => {
        if (!line) {
          schemaList.push(schema);
          schema = [];
          return;
        }
        schema.push(line);
      });
      schemaList.push(schema);
      return schemaList;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.schemaList = this.getInput();
    this.splitKeys();
  }

  splitKeys() {
    this.keys = [];
    this.locks = [];

    for (const schema of this.schemaList) {
      const counts = Array.from({ length: schema[0].length }, () => -1);
      for (const line of schema) {
        for (let i = 0; i < line.length; i++) {
          if (line[i] === "#") counts[i]++;
        }
      }
      if (schema[0] === "#####") this.locks.push(counts);
      else this.keys.push(counts);
    }
  }

  isValid(key, lock) {
    for (let i = 0; i < key.length; i++) {
      if (key[i] + lock[i] > 5) return false;
    }
    return true;
  }

  getCombo() {
    let valid = 0;
    for (const key of this.keys) {
      for (const lock of this.locks) {
        if (this.isValid(key, lock)) valid++;
      }
    }
    return valid;
  }
}

const code = new Code();
console.log("Day 25 part 1:", code.getCombo());
