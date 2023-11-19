const fs = require("fs");

class Game {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((row) => row.split(""));
    } catch (err) {
      throw err;
    }
  }
  constructor(useTest = false) {
    this.useTest = useTest;
    this.grid = this.getInput();
    this.width = this.grid[0].length;
    this.height = this.grid.length;
    this.dirMap = [
      [0, -1],
      [-1, 0],
      [1, 0],
      [0, 1],
    ];
    [this.players, this.globins, this.elves] = this.getPlayers();
    console.log([this.players, this.globins, this.elves]);
  }

  getPlayers() {
    const players = [];
    const globins = {};
    const elves = {};
    this.grid.forEach((row, j) => {
      row.forEach((char, i) => {
        if ("#.".includes(char)) return;
        const player = { pos: [i, j], attack: 3, health: 200, type: char };
        const key = `${i},${j}`;
        players.push([i, j]);
        if (char == "E") elves[key] = player;
        else if (char == "G") globins[key] = player;
      });
    });
    this.sortReadingOrder(players);
    return [players, globins, elves];
  }
  // list of coprds
  sortReadingOrder(list) {
    list.sort((a, b) => {
      if (a[1] == b[1]) return a[0] - b[0];
      return a[1] - b[1];
    });
  }

  isPath(x, y, barriers) {
    const inBound = x >= 0 && x < this.width && y >= 0 && y < this.height;
    if (!inBound) return false;
    const isWall = this.grid[y][x] === "#";
    const isBarrier = `${x},${y}` in barriers;
    return !isWall && !isBarrier;
  }

  bfs(coord, targets, barriers) {
    if (!this.isPath(coord[0], coord[1], barriers)) return Infinity;
    let q = [coord];
    let steps = 0;
    const seen = new Set();
    while (q.length > 0) {
      let temp = [];
      for (const [x, y] of q) {
        const key = `${x},${y}`;
        if (seen.has(key)) continue;
        seen.add(key);
        if (key in targets) return steps;
        for (const [dx, dy] of this.dirMap) {
          if (this.isPath(x + dx, y + dy, barriers)) {
            temp.push([x + dx, y + dy]);
          }
        }
      }
      q = temp;
      steps++;
    }
    return Infinity;
  }

  getNextStep(x, y, targets, barriers) {
    const closest = this.dirMap.map(([dx, dy]) => {
      return this.bfs([x + dx, y + dy], targets, barriers);
    });
    console.log(x, y, closest);

    const [minNumber, minIndex] = closest.reduce(
      ([minNum, minIdx], num, idx) => (num < minNum ? [num, idx] : [minNum, minIdx]),
      [Infinity, -1]
    );
    return minIndex === -1 ? [x, y] : [x + this.dirMap[minIndex][0], y + this.dirMap[minIndex][1]];
  }

  findInRange(x, y, targets) {
    let foundCoord = null;
    let foundTarget = this.dirMap.some(([dx, dy]) => {
      if (`${x + dx},${y + dy}` in targets && !foundCoord) {
        foundCoord = [x + dx, y + dy];
        return true;
      }
      return false;
    });
    return [foundTarget, foundCoord];
  }

  getOutcome() {
    let rounds = 0;
    while (rounds < 5 && Object.entries(this.elves).length !== 0 && Object.entries(this.globins).length !== 0) {
      const nextRound = [];
      this.players.forEach((coord) => {
        const [x, y] = coord;
        let player = `${x},${y}`;
        let targets, barriers;

        if (player in this.elves) {
          targets = this.globins;
          barriers = this.elves;
        } else {
          targets = this.elves;
          barriers = this.globins;
        }

        const [found, foundCoords] = this.findInRange(x, y, targets);
        if (found) {
          console.log(foundCoords, "in rnage", x, y, targets);
          // attack
          nextRound.push([x, y]);
        } else {
          const temp = barriers[player];
          delete barriers[player];
          const [newX, newY] = this.getNextStep(x, y, targets, barriers);
          console.log("nexy", newX, newY);
          const updatedPlayer = `${newX},${newY}`;
          barriers[updatedPlayer] = temp;
          barriers[updatedPlayer].pos = [newX, newY];
          nextRound.push([newX, newY]);
          this.elves = player in this.elves ? barriers : targets;
          this.globins = player in this.elves ? targets : barriers;
        }
      });
      this.players = nextRound;
      this.sortReadingOrder(this.players);
      rounds++;
      console.log("rounds", rounds, this.players, this.elves, this.globins);
    }
    console.log(this.elves, this.globins, rounds);
    return 1;
  }
}

const game = new Game(true);
console.log("Day 15 part 1:", game.getOutcome());
