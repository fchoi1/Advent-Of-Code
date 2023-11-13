const fs = require("fs");

class Light {
  constructor(pos, vel) {
    this.pos = pos;
    this.vel = vel;
    this.key = `${pos[0]},${pos[1]}`;
  }
  update() {
    this.pos[0] += this.vel[0];
    this.pos[1] += this.vel[1];
    this.key = `${this.pos[0]},${this.pos[1]}`;
  }
}

class Stars {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = /=<|, |>/;
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((item) => {
        const s = item.split(delimiters);
        return new Light([parseInt(s[1]), parseInt(s[2])], [parseInt(s[4]), parseInt(s[5])]);
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.starsList = this.getInput();
  }

  getDimensions() {
    return this.starsList.reduce(
      (prev, light) => {
        return [
          Math.min(prev[0], light.pos[0]),
          Math.max(prev[0], light.pos[0]),
          Math.min(prev[1], light.pos[1]),
          Math.max(prev[1], light.pos[1]),
        ];
      },
      [Infinity, 0, Infinity, 0]
    );
  }

  printGrid(lightSet) {
    const [minW, maxW, minH, maxH] = this.getDimensions();
    console.log(minW, maxW, minH, maxH);

    console.log("=========== print grid =========\n");
    // for (let j = minH; j < maxH; j++) {
    //   let string = "";
    //   for (let i = minW; i < maxW; i++) {
    //     let key = `${i},${j}`;
    //     string += lightSet.has(key) ? "#" : ".";
    //   }
    //   console.log(string);
    // }
  }
  getMessage() {
    let time = 0;
    let maxTime = this.useTest ? 10 : 20_000;
    let w = Infinity;
    let h = Infinity;
    let h = 0;
    while (time < maxTime) {
      const lightSet = new Set();
      this.starsList.forEach((light) => {
        light.update();
        lightSet.add(light.key);
      });

      if (time % 1_000 === 0) {
        const [minW, maxW, minH, maxH] = this.getDimensions();
        w = Math.min(w, maxW - minW);
        h = Math.min(h, maxH - minH);

        console.log(time, lightSet.size, [minW, maxW, minH, maxH], w, h);
        // this.printGrid(lightSet);
      }
      time++;
    }
    console.log([mw, w, mh, h]);

    return 1;
  }
}

const stars = new Stars();
console.log("Day 10 part 1:", stars.getMessage());
