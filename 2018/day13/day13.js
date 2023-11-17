const fs = require("fs");

class Cart {
  constructor(start, dir) {
    this.pos = start;
    this.dirIndex = ">v<^".indexOf(dir);
    this.turnIndex = 0;
    this.dirMap = [
      [1, 0],
      [0, 1],
      [-1, 0],
      [0, -1],
    ];
    this.turns = [-1, 0, 1];
  }

  updateCart(track) {
    if (track === "+") {
      this.dirIndex += this.turns[this.turnIndex % 3];
      this.turnIndex += 1;
    } else if (track === "/") {
      [1, 3].includes(this.dirIndex) ? this.dirIndex++ : this.dirIndex--;
    } else if (track === "\\") {
      [1, 3].includes(this.dirIndex) ? this.dirIndex-- : this.dirIndex++;
    }
    this.dirIndex = (this.dirIndex + 4) % 4;
    this.pos[0] += this.dirMap[this.dirIndex][0];
    this.pos[1] += this.dirMap[this.dirIndex][1];
  }
}

class Track {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").split(/\r?\n/);
      return data.map((row) => row.split(""));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.map = this.getInput();
    this.dirMap = [
      [">", [0, 1]],
      ["<", [0, -1]],
      ["^", [-1, 0]],
      ["v", [1, 0]],
    ];
    this.carts = this.findCarts();
    this.firstCrash = "";
    this.lastCart = "";
    this.checkCarts();
  }

  findCarts() {
    const carts = [];
    for (let j = 0; j < this.map.length; j++) {
      for (let i = 0; i < this.map[0].length; i++) {
        if (">v<^".includes(this.map[j][i])) carts.push(new Cart([i, j], this.map[j][i]));
      }
    }
    return carts;
  }

  sortCarts() {
    this.carts.sort((cartA, cartB) => {
      if (cartA.pos[1] == cartB.pos[1]) return cartA.pos[0] - cartB.pos[0];
      return cartA.pos[1] - cartB.pos[1];
    });
  }

  checkCarts() {
    let time = 0;
    let key;
    while (time < 15_000) {
      const seen = {};
      this.sortCarts();
      const removeCarts = [];
      this.carts.forEach((cart, i) => (seen[`${cart.pos[0]},${cart.pos[1]}`] = i));
      this.carts.forEach((cart, i) => {
        const [x, y] = cart.pos;
        delete seen[`${x},${y}`];
        cart.updateCart(this.map[y][x]);
        key = `${cart.pos[0]},${cart.pos[1]}`;
        if (key in seen) {
          if (!this.firstCrash) this.firstCrash = key;
          removeCarts.push(i, seen[key]);
        }
        seen[key] = i;
      });
      this.carts = this.carts.filter((_, index) => !removeCarts.includes(index));
      if (this.carts.length <= 1) return (this.lastCart = `${this.carts[0].pos[0]},${this.carts[0].pos[1]}`);
      time++;
    }
    console.log("Error");
  }

  getFirstCrash() {
    return this.firstCrash;
  }

  getLastCart() {
    return this.lastCart;
  }
}

const track = new Track();
console.log("Day 13 part 1:", track.getFirstCrash());
console.log("Day 13 part 2:", track.getLastCart());
