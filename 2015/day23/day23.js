const fs = require("fs");

class WizardSim {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const boss = {};
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      data.forEach((item) => {
        let [statName, value] = item.split(": ");
        if (statName === "Hit Points") statName = "Health";
        boss[statName] = parseInt(value);
      });
      return boss;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.boss = this.getInput();
    this.you = useTest;
  }


}

const wizardSim = new WizardSim();
console.log("Day 23 part 1:", wizardSim.getMinMana());
console.log("Day 23 part 2:", wizardSim.getMinMana(true));
