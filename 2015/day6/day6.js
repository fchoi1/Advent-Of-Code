const fs = require("fs");

class Lights {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const delimiters = / |,| through /;
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((config) => {
        const s = config.split(delimiters);
        if (s[0] !== "toggle") s.shift();
        return [s[0], [parseInt(s[1]), parseInt(s[2])], [parseInt(s[4]), parseInt(s[5])]];
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.instructions = this.getInput();
    this.lightOn = new Set();
    this.brightness = {};
    this.runLights();
  }

  updateLightSet(command, start, end) {
    const toggleLight = (i, j) => {
      const key = `${i},${j}`;
      this.lightOn.has(key) ? this.lightOn.delete(key) : this.lightOn.add(key);
    };

    for (let i = start[0]; i <= end[0]; i++) {
      for (let j = start[1]; j <= end[1]; j++) {
        const key = `${i},${j}`;
        const increment = ["off", "", "on", "toggle"].indexOf(command) - 1;
        if (!this.brightness[key] && command !== "off") this.brightness[key] = increment;
        else {
          this.brightness[key] += increment;
          if (this.brightness[key] < 0) {
            delete this.brightness[key];
          }
        }

        if (command === "on" || command === "off") {
          command === "on" ? this.lightOn.add(key) : this.lightOn.delete(key);
        } else if (command === "toggle") {
          toggleLight(i, j);
        }
      }
    }
  }

  runLights(useBrightness = false) {
    this.instructions.forEach(([command, start, end]) => {
      this.updateLightSet(command, start, end, useBrightness);
    });
  }

  getLightsOn() {
    return this.lightOn.size;
  }

  getBrightness() {
    return Object.values(this.brightness)
      .filter((val) => !isNaN(parseFloat(val)))
      .reduce((prev, val) => prev + parseFloat(val), 0);
  }
}

const lights = new Lights();
console.log("Day 6 part 1:", lights.getLightsOn());
console.log("Day 6 part 2:", lights.getBrightness());
// Total Runtime ~10.5
