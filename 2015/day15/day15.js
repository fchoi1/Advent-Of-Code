const fs = require("fs");

class Cookie {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = /: capacity |, durability |, flavor |, texture |, calories/;
    try {
      const ingredients = {};
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      data.forEach((row) => {
        const [ingredient, capacity, durability, flavor, texture, calories] = row.split(delimiters);
        ingredients[ingredient] = ingredients[ingredient] || {};
        ingredients[ingredient] = {
          capacity: parseInt(capacity),
          durability: parseInt(durability),
          flavor: parseInt(flavor),
          texture: parseInt(texture),
          calories: parseInt(calories),
        };
      });
      return ingredients;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.ingredients = this.getInput();
    this.combinations = this.makeCombination();
    this.teaspoons = 100;
    this.start = Object.keys(this.ingredients).length;
  }

  makeCombination() {
    return Object.fromEntries(Object.keys(this.ingredients).map((key) => [key, 1]));
  }

  getIngredientScore(combinations) {
    let totalCalories = 0;
    const totalStats = { capacity: 0, durability: 0, flavor: 0, texture: 0 };
    for (const [name, teaspoons] of Object.entries(combinations)) {
      const { capacity, durability, flavor, texture, calories } = this.ingredients[name];
      totalStats.capacity += teaspoons * capacity;
      totalStats.durability += teaspoons * durability;
      totalStats.flavor += teaspoons * flavor;
      totalStats.texture += teaspoons * texture;
      totalCalories += teaspoons * calories;
    }
    if (Object.values(totalStats).some((val) => val <= 0)) return [totalCalories, 0];
    return [totalCalories, Object.values(totalStats).reduce((score, val) => score * val, 1)];
  }

  getScore() {
    let curr = this.start;
    while (curr < this.teaspoons) {
      let currMax = 0;
      let currBestCombo;
      for (const ingredient in this.combinations) {
        let copyObj = { ...this.combinations };
        copyObj[ingredient] += 1;
        const [_, score] = this.getIngredientScore(copyObj);
        if (score > currMax) {
          currMax = score;
          currBestCombo = copyObj;
        }
      }
      this.combinations = currBestCombo;
      curr++;
    }
    return this.getIngredientScore(this.combinations)[1];
  }

  // Hardcoded
  getScore2() {
    let maxScore = 0;
    const hardCodeMin = 10;
    const hardCodeMax = 40;
    const possibleIngredients = Array.from({ length: hardCodeMax - hardCodeMin }, (_, index) => index + hardCodeMin);

    possibleIngredients.forEach((Frosting) => {
      possibleIngredients.forEach((Candy) => {
        possibleIngredients.forEach((Butterscotch) => {
          possibleIngredients.forEach((Sugar) => {
            if (Frosting + Candy + Butterscotch + Sugar === 100) {
              const combo = { Frosting, Candy, Butterscotch, Sugar };
              const [cal, score] = this.getIngredientScore(combo);
              if (cal === 500 && score > maxScore) {
                maxScore = Math.max(score, maxScore);
              }
            }
          });
        });
      });
    });
    return maxScore;
  }
}

const cookie = new Cookie();
console.log("Day 15 part 1:", cookie.getScore());
console.log("Day 15 part 2:", cookie.getScore2());
