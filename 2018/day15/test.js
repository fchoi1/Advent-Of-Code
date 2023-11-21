#!/usr/bin/env node

const fs = require("fs");

let contents = fs.readFileSync("input.txt", "utf8").trim();
// let contents = fs.readFileSync("input-test.txt", "utf8").trim();

function Game(boardString, elvesAp) {
  this.height = boardString.length;
  this.width = boardString[0].length;
  this.dimensions = [this.height, this.width];
  this.board = new Array(this.height).fill(null).map((a) => new Array(this.width).fill(null));

  this.wallObject = "#";
  this.unitObject = {
    hp: 200,
    ap: 3,
  };

  if (elvesAp == null) elvesAp = 3;
  this.elveUnitObject = Object.assign({}, this.unitObject);
  this.elveUnitObject.ap = elvesAp;

  this.rounds = 0;
  this.fullRounds = null;
  this.elves = [];
  this.goblins = [];
  let unit;

  for (let i = 0; i < this.height; i++)
    for (let j = 0; j < this.width; j++)
      switch (boardString[i][j]) {
        case "#":
          this.board[i][j] = this.wallObject;
          break;
        case ".":
          break;
        case "G":
          unit = Object.assign({ race: "G", position: [i, j], history: [], pos: `${j},${i}` }, this.unitObject);
          this.goblins.push(unit);
          this.board[i][j] = unit;
          break;
        case "E":
          unit = Object.assign({ race: "E", position: [i, j], history: [], pos: `${j},${i}` }, this.elveUnitObject);
          this.elves.push(unit);
          this.board[i][j] = unit;
          break;
        default:
          throw "Unknown symbol " + this.board[i][j];
      }
}

let directions = [
  [-1, 0],
  [0, -1],
  [0, 1],
  [1, 0],
];

Game.prototype.findAdjancedPoints = function (_position) {
  let outputArray = [];

  for (let d in directions) {
    let position = _position.slice();
    for (let j in position) {
      position[j] += directions[d][j];
      if (position[j] < 0 || position[j] >= this.dimensions[j]) {
        position = null;
        break;
      }
    }

    outputArray.push(position);
  }

  return outputArray;
};

Game.prototype.findAdjancedEmptyPoints = function (_position, outputArray) {
  if (outputArray == null) outputArray = [];

  for (let d in directions) {
    let position = _position.slice();
    for (let j in position) {
      position[j] += directions[d][j];
      if (position[j] < 0 || position[j] >= this.dimensions[j]) {
        position = null;
        break;
      }
    }

    if (position && this.board[position[0]][position[1]] == null) outputArray.push(position);
  }

  return outputArray;
};

Game.prototype.findDistancies = function (position) {
  let distancies = new Array(this.height).fill(null).map((v) => new Array(this.width).fill(null));

  let positions = [position];
  let distance = 1;
  while (positions.length > 0) {
    let newDistancies = [];
    for (let i in positions) {
      let p = positions[i];
      if (distancies[p[0]][p[1]] == null) {
        distancies[p[0]][p[1]] = distance;
        newDistancies.push(...this.findAdjancedEmptyPoints(p));
      }
    }
    positions = newDistancies;
    distance++;
  }
  return distancies;
};

Game.prototype.unitMove = function (unit) {
  let enemies = unit.race == "E" ? this.goblins : this.elves;

  let inRange = [];
  for (let i in enemies) {
    this.findAdjancedEmptyPoints(enemies[i].position, inRange);
  }

  let distancies = this.findDistancies(unit.position);

  let reachable = inRange
    .map((e) => [...e, distancies[e[0]][e[1]]])
    .filter((e) => e[2] !== null)
    .sort((a, b) => a[2] - b[2]);

  if (reachable.length == 0) return;

  let smallestDistance = reachable[0][2];
  let bests = reachable
    .filter((e) => e[2] == smallestDistance)
    .map((e) => [...e, e[1] + e[0] * this.width])
    .sort((a, b) => a[3] - b[3]);
  let best = bests[0];

  let backwardDistancies = this.findDistancies(best);

  let directions = this.findAdjancedEmptyPoints(unit.position).filter((e) => backwardDistancies[e[0]][e[1]] !== null);
  // console.log("\n")
  //   console.log(this.showDistancies(backwardDistancies));
  let bestDirection = directions.shift();
  for (let i in directions) {
    let d = directions[i];
    if (backwardDistancies[d[0]][d[1]] < backwardDistancies[bestDirection[0]][bestDirection[1]]) bestDirection = d;
  }
  console.log(unit.position[1], unit.position[0], [bestDirection[1], bestDirection[0]]);

  this.board[unit.position[0]][unit.position[1]] = null;
  this.board[bestDirection[0]][bestDirection[1]] = unit;
  unit.position = bestDirection;
  unit.history.push(`${bestDirection[1]},${bestDirection[0]}`);
  // console.log(unit);
};

Game.prototype.unitAttack = function (unit) {
  let enemyRace = unit.race == "E" ? "G" : "E";
  let enemyObject = enemyRace == "E" ? "elves" : "goblins";
  let enemies = [];
  let unitAdjancesPoints = this.findAdjancedPoints(unit.position);

  for (let i in unitAdjancesPoints) {
    let p = unitAdjancesPoints[i];
    let e = this.board[p[0]][p[1]];
    if (e == null) continue;

    if (typeof e == "object" && e.race == enemyRace) {
      enemies.push(e);
    }
  }

  if (enemies.length == 0) return;

  let choosedEnemy = enemies[0];
  for (let i = 1; i < enemies.length; i++) {
    if (enemies[i].hp < choosedEnemy.hp) choosedEnemy = enemies[i];
  }

  choosedEnemy.hp -= unit.ap;
  console.log(
    "unit attacked",
    `${choosedEnemy.position[1]},${choosedEnemy.position[0]}`,
    "by",
    `${unit.position[1]},${unit.position[0]}`
  );
  if (choosedEnemy.hp <= 0) {
    let unitsList = this[enemyObject];
    let i = unitsList.indexOf(choosedEnemy);
    this[enemyObject].splice(i, 1);
    this.board[choosedEnemy.position[0]][choosedEnemy.position[1]] = null;

    if (this[enemyObject].length == 0) {
      this.fullRounds = this.rounds;
    }
  }
};

Game.prototype.unitTurn = function (unit) {
  let unitAdjancesPoints = this.findAdjancedPoints(unit.position);
  let enemies = unit.race == "E" ? "G" : "E";

  let enemy = null;
  for (let i in unitAdjancesPoints) {
    let p = unitAdjancesPoints[i];
    let e = this.board[p[0]][p[1]];
    if (e == null) continue;

    if (typeof e == "object" && e.race == enemies) {
      enemy = e;
      break;
    }
  }

  if (enemy == null) this.unitMove(unit);
  this.unitAttack(unit);
};

Game.prototype.showDistancies = function (distancies) {
  let board = this.prepareBoardArray();
  for (let y in distancies) {
    for (let x in distancies[y]) {
      if (distancies[y][x] != null) {
        board[y][x] = distancies[y][x].toString();
      }
    }
  }

  return board.map((l) => l.join(",")).join("\n");
};

Game.prototype.prepareBoardArray = function () {
  let board = new Array(this.height).fill(null).map((e) => new Array(this.width).fill("#"));
  for (let y in this.board) {
    for (let x in this.board[y]) {
      let e = this.board[y][x];
      if (e == null) board[y][x] = ".";
      else if (typeof e === "object") board[y][x] = e.race;
    }
  }
  return board;
};

Game.prototype.showBoard = function () {
  let board = this.prepareBoardArray();
  return board.map((l) => l.join("")).join("\n");
};

Game.prototype.showUnits = function () {
  let units = [...this.elves, ...this.goblins].sort(
    (a, b) => a.position[0] - b.position[0] || a.position[1] - b.position[1]
  );
  return units.map((u) => u.race + "(" + u.hp + ")").join("\n");
};

Game.prototype.round = function () {
  let units = [...this.elves, ...this.goblins].sort(
    (a, b) => a.position[0] - b.position[0] || a.position[1] - b.position[1]
  );

  for (let i = 0; i < units.length - 1; i++) {
    if (units[i].hp <= 0) continue;
    this.unitTurn(units[i]);
    if (this.rounds == 38 || this.rounds == 39) {
    //   console.log(units[i].position, units[i].race);
    }
  }

  this.rounds++;
  let li = units.length - 1;
  if (units[li].hp <= 0 && this.fullRounds != null) this.fullRounds = this.rounds;
  this.unitTurn(units[li]);

  let countingUnits;
  if (this.elves.length == 0) countingUnits = this.goblins;
  else if (this.goblins.length == 0) {
    countingUnits = this.elves;
  }

  if (countingUnits == null) return null;
  console.log(countingUnits);
  return this.fullRounds * countingUnits.map((e) => e.hp).reduce((total, v) => total + v);
};

Game.prototype.execute = function () {
  let gameResult = null;
  do {
    gameResult = this.round();

    console.log("Round ", this.rounds);
    // console.log(game.showBoard());
    // console.log(game.showUnits());
  } while (gameResult == null);
  console.log(gameResult);
  return gameResult;
};

Game.prototype.executeTillElveDeath = function () {
  let gameResult = null;
  let totalElves = this.elves.length;
  do {
    gameResult = this.round();
    if (totalElves > this.elves.length) {
      return null;
    }
  } while (gameResult == null);
  return gameResult;
};

function findLowestElvesAp(board) {
  let ap = 3;
  let gameResult = null;
  do {
    ap++;
    gameResult = new Game(board, ap).executeTillElveDeath();
  } while (gameResult == null);
  return gameResult;
}

console.log("Part One:", new Game(contents.split("\n")).execute());
// console.log("Part Two:", findLowestElvesAp(contents.split("\n")));
