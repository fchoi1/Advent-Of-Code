const fs = require("fs");

class Room {
  constructor(location, { north = null, south = null, east = null, west = null } = {}) {
    if (north) north.doors.south = this;
    if (south) south.doors.north = this;
    if (east) east.doors.west = this;
    if (west) west.doors.east = this;
    this.loc = location;
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
      E: [-1, 0],
      S: [0, 1],
      W: [1, 0],
      N: [0, -1],
    };
    this.start = new Room([0, 0], {});
  }
  runRoute(char, room) {
    let sym = this.route[char];
    while (sym !== "$") {
      let sym = this.route[char];
      if (sym === "(") {
        const [newChar, subRoutes] = this.getRoutes(char + 1);
        subRoutes.forEach((route) => {
          const newRoom = this.checkRooms(currRoom, route);
          this.runRoute(newChar, newRoom);
        });
        break;
      }
      room = this.getNewRoom(room, sym);
      char++;
    }
  }

  getNewRoom(room, dir) {
    const nextDir = this.dirMap[dir];
    if (room.doors[nextDir]) room = room.doors[nextDir];
    else {
      const [dx, dy] = this.dirCoord[dir];
      room = new Room([room.loc[0] + dx, room.loc[1] + dy], { [nextDir]: room });
    }
    return room;
  }

  checkRooms(room, path) {
    path.forEach((dir) => {
      room = this.getNewRoom(room, dir);
    });
    return room;
  }

  getRoutes(char, currRoute) {
    const routes = [];
    let sym = this.route[char];
    let temp = "";
    while (char < this.route.length) {
      sym = this.route[char];
      console.log(sym, char, this.route);
      if ("|)".includes(sym)) {
        routes.push(currRoute + temp);
        temp = "";
        if (sym === ")") break;
      } else if (sym === "(") {
        const nested = this.getRoutes(char + 1, temp);
        char = nested[0];
        nested[1].forEach((subRoute) => routes.push(currRoute + subRoute));
        temp = ""
      } else temp += sym;
      char++;
    }
    // routes.push(currRoute + temp);
    console.log("return ", char, routes);
    return [char+1, routes];
  }

  runProgram() {
    this.route = "(NEEE|SSE(EE|N|)|)";
    console.log(this.getRoutes(0, ""));
    return 1;
  }
}

const roomMap = new RoomMap();
console.log("Day 20 part 1:", roomMap.runProgram());
