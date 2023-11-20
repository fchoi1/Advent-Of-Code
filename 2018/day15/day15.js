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
  }

  getPlayers() {
    const players = [];
    const globins = {};
    const elves = {};
    this.grid.forEach((row, j) => {
      row.forEach((char, i) => {
        if ("#.".includes(char)) return;
        const key = `${i},${j}`;
        const player = { attack: 3, health: 200, type: char, pos: key };
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
    let found = [];
    if (!this.isPath(coord[0], coord[1], barriers)) return [];
    let q = [coord];
    const seen = new Set();
    while (q.length > 0) {
      let temp = [];
      for (const [x, y] of q) {
        const key = `${x},${y}`;
        if (key in targets) found.push([x, y]);
        if (seen.has(key)) continue;
        seen.add(key);
        for (const [dx, dy] of this.dirMap) {
          if (this.isPath(x + dx, y + dy, barriers)) temp.push([x + dx, y + dy]);
        }
      }
      if (found.length > 0) {
        this.sortReadingOrder(found);
        return found[0];
      }
      q = temp;
    }
    return [];
  }

  generateAdj(targets) {
    const targetSet = {};
    Object.keys(targets).forEach((coord) => {
      const [x, y] = coord.split(",").map((str) => parseInt(str));
      this.dirMap.forEach(([dx, dy]) => (targetSet[`${x + dx},${y + dy}`] = null));
    });
    return targetSet;
  }

  getNextStep(x, y, targets, barriers) {
    const closestTarget = this.bfs([x, y], this.generateAdj(targets), barriers);
    if (closestTarget.length === 0) return [x, y];
    const adjTargets = {};
    this.dirMap.forEach(([dx, dy]) => (adjTargets[`${x + dx},${y + dy}`] = null));
    return this.bfs(closestTarget, adjTargets, barriers);
  }

  findInRange(x, y, targets) {
    let foundCoords = [];
    let foundTarget = false;
    this.dirMap.forEach(([dx, dy]) => {
      if (`${x + dx},${y + dy}` in targets) {
        foundCoords.push(`${x + dx},${y + dy}`);
        foundTarget = true;
      }
    });
    return [foundTarget, foundCoords];
  }

  getLowsestHealth(target, foundCoords) {
    return foundCoords.reduce(
      (prev, coords) => {
        if (target[coords].health < prev[0]) return [target[coords].health, coords];
        return prev;
      },
      [Infinity, ""]
    );
  }

  getScore(rounds) {
    let score = 0;
    if (Object.entries(this.elves).length !== 0 && Object.entries(this.globins).length === 0) {
      for (let elf of Object.values(this.elves)) score += elf.health;
    } else if (Object.entries(this.globins).length !== 0 && Object.entries(this.elves).length === 0) {
      for (let globin of Object.values(this.globins)) score += globin.health;
    }
    return score * rounds;
  }

  getOutcome() {
    let rounds = 0;
    let gameover = false;
    while (rounds < 100) {
      let nextRound = [];
      this.players.forEach((coord) => {
        if (gameover) return;
        let [x, y] = coord;
        let player = `${x},${y}`;
        let targets, barriers;

        if (player in this.elves) {
          targets = this.globins;
          barriers = this.elves;
        } else if (player in this.globins) {
          targets = this.elves;
          barriers = this.globins;
        } else return;
        if (Object.keys(targets).length === 0) {
          gameover = true;
          return;
        }
        let [found, foundCoords] = this.findInRange(x, y, targets);
        if (!found) {
          const temp = barriers[player];
          delete barriers[player];
          [x, y] = this.getNextStep(x, y, targets, barriers);
          const updatedPlayer = `${x},${y}`;
          barriers[updatedPlayer] = temp;
          [found, foundCoords] = this.findInRange(x, y, targets);
        }
        if (found) {
          const [_, lowestHealthcoord] = this.getLowsestHealth(targets, foundCoords);
          targets[lowestHealthcoord].health -= 3;
          if (targets[lowestHealthcoord].health <= 0) {
            delete targets[lowestHealthcoord];
            nextRound = nextRound.filter(([x, y]) => `${x},${y}` !== lowestHealthcoord);
          }
        }
        nextRound.push([x, y]);
        this.elves = player in this.elves ? barriers : targets;
        this.globins = player in this.elves ? targets : barriers;
      });
      this.players = nextRound;
      this.sortReadingOrder(this.players);
      if (gameover) break;
      rounds++;
    }
    return this.getScore(rounds);
  }
}

const game = new Game();
console.log("Day 15 part 1:", game.getOutcome());
