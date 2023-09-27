const fs = require("fs");

class Medicine {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data.reduce(
        ([molecules, reverseMolecules, dna], row) => {
          const [source, target] = row.split(" => ");
          if (source === "") return [molecules, reverseMolecules, dna];
          if (!target) return [{ ...molecules }, { ...reverseMolecules }, source];
          return [
            { ...molecules, [source]: [...(molecules[source] || []), target] },
            { ...reverseMolecules, [target]: [...(reverseMolecules[target] || []), source] },
            dna,
          ];
        },
        [{}, ""]
      );
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.molecules, this.reverseMolecules, this.dna] = this.getInput();
    this.medicine = this.dna;
    this.dna = this.dna.split("");
    this.combinations = new Set();
  }

  countCombinations() {
    let prev = "";
    let tempStr;
    this.dna.forEach((char, index) => {
      if (this.molecules[char]) {
        for (const str of this.molecules[char]) {
          tempStr = [...this.dna];
          tempStr.splice(index, 1, str);
          this.combinations.add(tempStr.join(""));
        }
      } else if (this.molecules[prev + char]) {
        for (const str of this.molecules[prev + char]) {
          tempStr = [...this.dna];
          tempStr.splice(index - 1, 2, str);
          this.combinations.add(tempStr.join(""));
        }
      } else {
        prev = char;
      }
    });
  }

  getCombinations() {
    this.countCombinations();
    return this.combinations.size;
  }

  searchMedicine(currString, steps, visited) {
    if (visited.has(currString)) return Infinity;
    visited.add(currString);

    if (currString === "e") return steps;

    let minSteps = Infinity;
    let newStr = currString.split("");
    for (const [replacement, molecule] of Object.entries(this.reverseMolecules)) {
      if (currString.includes(replacement) && replacement !== "e") {
        newStr.splice(currString.indexOf(replacement), replacement.length, molecule);
        minSteps = Math.min(this.searchMedicine(newStr.join(""), steps + 1, visited), minSteps);
        break;
      }
    }
    return minSteps;
  }
  getFewestSteps() {
    return this.searchMedicine(this.medicine, 0, new Set());
  }
}

const medicine = new Medicine();
console.log("Day 19 part 1:", medicine.getCombinations());
console.log("Day 19 part 2:", medicine.getFewestSteps());
