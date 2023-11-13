const fs = require("fs");

class Marble {
  constructor(val) {
    this.val = val;
    this.next = null;
    this.prev = null;
  }
}

class MarbleGame {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0].split(" ");
      return [parseInt(data[0]), parseInt(data[6])];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    [this.players, this.marbles] = this.getInput();
  }

  getHighScore(multipy) {
    const loops = multipy ? this.marbles * 100 : this.marbles;
    this.playerList = Array(this.players).fill(0);
    let node = new Marble(0);
    node.next = node;
    node.prev = node;
    let seventh, currPlayer;
    for (let i = 1; i < loops; i++) {
      currPlayer = i % this.players;

      if (i % 23 == 0) {
        seventh = node;
        for (let i = 0; i <= 7; i++) seventh = seventh.prev;
        this.playerList[currPlayer] += i + seventh.next.val;
        node = seventh.next.next;
        seventh.next = node;
        node.prev = seventh;
      } else {
        let newMarble = new Marble(i);
        let temp = node.next.next;
        // Swap
        node.next.next = newMarble;
        newMarble.next = temp;
        newMarble.prev = node.next;
        temp.prev = newMarble;
        node = newMarble;
      }
    }
    return this.playerList.reduce((prev, curr) => Math.max(prev, curr), 0);
  }
}

const marbleGame = new MarbleGame();
console.log("Day 9 part 1:", marbleGame.getHighScore());
console.log("Day 9 part 2:", marbleGame.getHighScore(true));
