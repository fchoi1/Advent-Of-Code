const fs = require("fs");

class Recipe {
  constructor(val, next = null, prev = null) {
    this.next = next;
    this.prev = prev;
    this.val = val;
  }
}

class Chocolate {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0];
      return [data, parseInt(data)];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.strRecipes, this.recipes] = this.getInput();
    this.length = this.strRecipes.length;
    this.runRecipes();
  }

  setup() {
    const first = new Recipe(3);
    const second = new Recipe(7);
    first.next = first.prev = second;
    second.next = second.prev = first;
    return [first, second];
  }

  getLastTen(node) {
    let str = "";
    for (let i = 0; i < 10; i++) {
      node = node.prev;
      str = String(node.val) + str;
    }
    return str;
  }

  runRecipes() {
    let [root, second] = this.setup();
    let first = root;
    let end = second;
    let length = 2;
    let foundRecipe = false;
    const target = 10 + this.recipes;
    while (length < target || !foundRecipe) {
      const val1 = first.val;
      const val2 = second.val;
      const sum = val1 + val2;
      const digits = sum.toString().split("").map(Number);
      for (const digit of digits) {
        const newNode = new Recipe(digit, root, end);
        end.next = newNode;
        root.prev = newNode;
        end = newNode;
        length++;
      }
      for (let i = 0; i < val1 + 1; i++) first = first.next;
      for (let i = 0; i < val2 + 1; i++) second = second.next;

      let currScore = this.getLastTen(root);
      let currScore2 = sum > 9 ? this.getLastTen(root.prev) : "";
      const found1 = currScore.slice(0, this.length) === this.strRecipes && !this.count;
      const found2 = currScore2.slice(0, this.length) === this.strRecipes && !this.count;

      if (found1 || found2) {
        foundRecipe = true;
        this.count = found1 ? length - 10 : length - 11;
      }
      if (length === target) this.score = this.getLastTen(root); // lucky
    }
  }

  getScore() {
    return this.score;
  }

  countInputScore() {
    return this.count;
  }
}

const chocolate = new Chocolate();
console.log("Day 14 part 1:", chocolate.getScore());
console.log("Day 14 part 2:", chocolate.countInputScore());
// Total Runtime 9.3s
