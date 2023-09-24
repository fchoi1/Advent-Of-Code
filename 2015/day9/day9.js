const fs = require("fs");

class Locations {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const locationMap = {};
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      data.forEach((route) => {
        const [locations, distance] = route.split(" = ");
        const [location1, location2] = locations.split(" to ");
        locationMap[location1] = { ...(locationMap[location1] || {}), [location2]: parseInt(distance) };
        locationMap[location2] = { ...(locationMap[location2] || {}), [location1]: parseInt(distance) };
      });
      return locationMap;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.routes = this.getInput();
    this.shortest = Number.POSITIVE_INFINITY;
    this.longest = Number.NEGATIVE_INFINITY;
    this.destinations = Object.keys(this.routes).length;
    this.calculateDistance();
  }

  // dfs?
  getShortestRoute(currlocation, totalDistance, visited) {
    visited.add(currlocation);
    if (visited.size === this.destinations) {
      this.shortest = Math.min(this.shortest, totalDistance);
      this.longest = Math.max(this.longest, totalDistance);
      return;
    }
    const nextLocations = this.routes[currlocation];
    for (const location in nextLocations) {
      if (!visited.has(location)) {
        this.getShortestRoute(location, totalDistance + nextLocations[location], new Set(visited));
      }
    }
  }

  calculateDistance() {
    Object.keys(this.routes).forEach((location) => {
      this.getShortestRoute(location, 0, new Set());
    });
  }

  getShortest() {
    return this.shortest;
  }
  getLongest() {
    return this.longest;
  }
}

const locations = new Locations();
console.log("Day 9 part 1:", locations.getShortest());
console.log("Day 9 part 2:", locations.getLongest());
