const fs = require("fs");

class Knights {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = / would | happiness units by sitting next to |\./;
    try {
      const members = {};
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      data.forEach((rule) => {
        const [person1, change, person2] = rule.split(delimiters);
        const happinessChange = (change.split(" ")[0] === "gain" ? 1 : -1) * parseInt(change.split(" ")[1]);
        members[person1] = members[person1] || {};
        members[person1][person2] = happinessChange;
      });
      return members;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.memebers = this.getInput();
    this.happiness = 0;
    this.memberLength = Object.keys(this.memebers).length;
  }

  calculateHappiness(personList) {
    let happiness = 0;
    personList.forEach((person, i) => {
      const prev = personList[(i - 1 + personList.length) % personList.length];
      const next = personList[(i + 1 + personList.length) % personList.length];
      if (this.memebers[person][prev]) happiness += this.memebers[person][prev];
      if (this.memebers[person][next]) happiness += this.memebers[person][next];
    });
    return happiness;
  }

  getHappiness(person, personList) {
    if (personList.includes(person)) return;
    personList.push(person);
    if (personList.length === this.memberLength) {
      this.happiness = Math.max(this.happiness, this.calculateHappiness(personList));
      return;
    }
    for (const person in this.memebers) {
      this.getHappiness(person, personList.slice());
    }
  }

  getHappinessChange(includeYourself) {
    this.happiness = 0;
    if (includeYourself) {
      this.memebers["you"] = {};
      this.memberLength = Object.keys(this.memebers).length;
    }
    this.getHappiness(Object.keys(this.memebers)[0], []);
    return this.happiness;
  }
}

const knights = new Knights();
console.log("Day 13 part 1:", knights.getHappinessChange());
console.log("Day 13 part 2:", knights.getHappinessChange(true));
