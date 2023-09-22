const fs = require("fs");

class WrappingPaper {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      return data.map((dimension) => {
        return dimension.split("x").map((str) => parseInt(str));
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.gifts = this.getInput();
  }

  getSurfaceArea(l, w, h) {
    const areas = [2 * l * w, 2 * w * h, 2 * h * l];
    return areas[0] + areas[1] + areas[2] + Math.min(...areas) / 2;
  }

  getribbon(l, w, h) {
    const perimeters = [2 * (l + w), 2 * (w + h), 2 * (h + l)];
    return l * w * h + Math.min(...perimeters);
  }

  getRibbonLength() {
    return this.gifts.reduce((length, gift) => length + this.getribbon(...gift), 0);
  }

  getArea() {
    return this.gifts.reduce((area, gift) => area + this.getSurfaceArea(...gift), 0);
  }
}

const wrappingPaper = new WrappingPaper();
console.log("Day 2 part 1:", wrappingPaper.getArea());
console.log("Day 2 part 2:", wrappingPaper.getRibbonLength());
