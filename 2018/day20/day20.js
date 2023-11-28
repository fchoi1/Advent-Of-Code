const fs = require("fs");

class Room {
  constructor(location, { north = null, south = null, east = null, west = null } = {}) {
    if (north) north.doors.north = this;
    if (south) south.doors.south = this;
    if (east) east.doors.east = this;
    if (west) west.doors.west = this;
    this.loc = location;
    this.key = `${location[0]},${location[1]}`;
    this.doors = {
      north: south,
      south: north,
      east: west,
      west: east,
    };
  }
}

class RoomMap {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      return fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0];
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.route = this.getInput();
    this.dirMap = {
      E: "east",
      S: "south",
      W: "west",
      N: "north",
    };
    this.dirCoord = {
      E: [1, 0],
      S: [0, 1],
      W: [-1, 0],
      N: [0, -1],
    };
    this.steps = 0;
    this.start = new Room([0, 0], {});
    this.rooms = { "0,0": this.start };
    this.dim = { max: { x: 0, y: 0 }, min: { x: Infinity, y: Infinity } };
    this.runRoute(1, this.start);
    console.log(this.dim);
  }

  runRoute(char, room) {
    while (char < this.route.length) {
      let sym = this.route[char];
      if (sym === "(") {
        const [newChar, subRoutes] = this.getRoutes(char + 1, "");
        subRoutes.forEach((route) => {
          const newRoom = this.checkRooms(room, route);
          this.runRoute(newChar, newRoom);
        });
        return;
      }
      if (sym === "$") return;
      room = this.getNewRoom(room, sym);
      char++;
    }
  }

  getNewRoom(room, dir) {
    const nextDir = this.dirMap[dir];
    const [dx, dy] = this.dirCoord[dir];
    if (room.doors[nextDir]) room.doors[nextDir];
    const newRoom = new Room([room.loc[0] + dx, room.loc[1] + dy], { [nextDir]: room });
    if (room.loc[0] + dx > this.dim.max.x) this.dim.max.x = room.loc[0] + dx;
    if (room.loc[1] + dy > this.dim.max.y) this.dim.max.y = room.loc[1] + dy;
    if (room.loc[0] + dx < this.dim.min.x) this.dim.min.x = room.loc[0] + dx;
    if (room.loc[1] + dy < this.dim.min.y) this.dim.min.y = room.loc[1] + dy;

    this.rooms[newRoom.key] = newRoom;
    return newRoom;
  }

  checkRooms(room, path) {
    path.split("").forEach((dir) => (room = this.getNewRoom(room, dir)));
    return room;
  }

  getRoutes(char, currRoute) {
    const routes = [];
    let sym = this.route[char];
    let temp = "";
    let nested = [];
    while (char < this.route.length) {
      sym = this.route[char];
      // console.log(temp, sym, char);
      if ("|)".includes(sym)) {
        if (nested[1]) nested[1].forEach((subRoute) => routes.push(currRoute + subRoute + temp)); // not yet
        else routes.push(currRoute + temp);
        // console.log("temp", temp, nested, routes);
        temp = "";
        if (sym === ")") break;
      } else if (sym === "(") {
        nested = this.getRoutes(char + 1, temp);
        char = nested[0];
        temp = this.route[char];
        if (temp === ")") {
          if (nested[1]) nested[1].forEach((subRoute) => routes.push(currRoute + subRoute)); // not yet
          break;
        }
      } else temp += sym;
      char++;
    }
    // routes.push(currRoute + temp);
    // console.log("return ", char, routes);
    return [char + 1, routes];
  }

  printGrid() {
    let top, bot, mid, key;
    for (let j = this.dim.min.y - 1; j < this.dim.max.y + 1; j++) {
      top = "";
      bot = "";
      mid = "";
      for (let i = this.dim.min.x - 1; i < this.dim.max.x + 1; i++) {
        key = `${i},${j}`;
        top += this.rooms[key]?.doors.north ? "#-#" : "###";
        bot += this.rooms[key]?.doors.south ? "#-#" : "###";
        if (key === "0,0") mid += "000";
        else if (this.rooms[key]?.doors.west && this.rooms[key]?.doors.east) mid += "|.|";
        else if (!this.rooms[key]?.doors.west && !this.rooms[key]?.doors.east) mid += "#.#";
        else if (this.rooms[key]?.doors.west) mid += "|.#";
        else if (this.rooms[key]?.doors.east) mid += "#.|";
        else mid += "###";
      }
      console.log(top);
      console.log(mid);
      console.log(bot);
    }
  }

  getFurthestRoom() {
    this.printGrid();
    this.getFurthestSteps(this.start, 0, new Set());
    console.log(this.furthest);
    return this.steps;
  }

  getFurthestSteps(room, steps, seen) {
    if (seen.has(room.key)) return [0, room];
    seen.add(room.key);
    Object.values(room.doors).forEach((door) => {
      if (door) {
        const [maxSteps, endRoom] = this.getFurthestSteps(door, steps + 1, seen);
        if (maxSteps > this.steps) {
          this.steps = maxSteps;
          this.furthest = endRoom;
        }
      }
    });
    return [steps, room];
  }
}

const roomMap = new RoomMap();
console.log("Day 20 part 1:", roomMap.getFurthestRoom());
