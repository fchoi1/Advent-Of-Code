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
  addOpposite(dir, room) {
    const dirMap = ["east", "south", "west", "north"];
    this.doors[dirMap["WNES".indexOf(dir)]] = room;
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
    this.routeList = [];
    this.start = new Room([0, 0], {});
    this.rooms = { "0,0": this.start };
    this.addRoutes(this.start.key, 1, []);
    [this.steps, this.roomCount] = this.analyzeRoom(this.start);
  }

  addRoutes(startLoc, pos, stack) {
    let room = this.rooms[startLoc];
    for (let char = pos; char < this.route.length; char++) {
      let sym = this.route[char];
      if (sym === "$") return;
      else if ("ESWN".includes(sym)) room = this.getNewRoom(room, sym);
      else if (sym === "(") {
        stack.push(room.key);
        this.addRoutes(room.key, char + 1, stack);
        return;
      } else if (sym === "|") {
        room = this.rooms[stack.slice(-1)[0]];
      } else if (sym === ")") stack.pop();
    }
  }

  getNewRoom(room, dir) {
    const dirMap = ["east", "south", "west", "north"];
    const dirCoord = [
      [1, 0],
      [0, 1],
      [-1, 0],
      [0, -1],
    ];
    const nextDir = dirMap["ESWN".indexOf(dir)];
    const [dx, dy] = dirCoord["ESWN".indexOf(dir)];
    const key = `${room.loc[0] + dx},${room.loc[1] + dy}`;
    if (this.rooms[key]) {
      room.doors[nextDir] = this.rooms[key];
      this.rooms[key].addOpposite(dir, room);
      return this.rooms[key];
    }
    const newRoom = new Room([room.loc[0] + dx, room.loc[1] + dy], { [nextDir]: room });
    this.rooms[newRoom.key] = newRoom;
    return this.rooms[newRoom.key];
  }

  analyzeRoom(room) {
    let q = [room];
    const seen = new Set();
    let over1000 = new Set();
    let steps = 0;
    const doorCount = this.useTest ? 16 : 1000;
    while (q.length > 0) {
      let temp = [];
      for (const room of q) {
        seen.add(room.key);
        Object.values(room.doors).forEach((door) => {
          if (door && !seen.has(door.key)) temp.push(door);
        });
      }
      q = temp;
      steps++;
      if (steps >= doorCount) over1000 = new Set([...over1000, ...temp.map((door) => door.key)]);
    }
    return [steps - 1, over1000.size];
  }

  getFurthestRoom() {
    return this.steps;
  }

  getDoorCount() {
    return this.roomCount;
  }
}

const roomMap = new RoomMap();
console.log("Day 20 part 1:", roomMap.getFurthestRoom());
console.log("Day 20 part 2:", roomMap.getDoorCount());
// Total runtime 0.63s
