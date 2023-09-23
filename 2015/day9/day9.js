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
        locationMap[location1] = { ...(locationMap[location1] || {}), [location2]: distance };
        locationMap[location2] = { ...(locationMap[location2] || {}), [location1]: distance };
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
    this.destinations = Object.keys(this.routes).length;
    console.log(this.routes, this.destinations);
  }

  // dfs?
  getShortestRoute(currlocation, totalDistance, visited) {
    console.log(visited);
    if (this.visited.size === this.destinations) {
      this.shortest = Math.min(this.shortest, totalDistance);
      return;
    }
    visited.add(currlocation);
    const nextLocations = this.routes[currlocation];
    for (const [location, distance] of nextLocations) {
      if (!visited.has(location)) {
        this.getShortestRoute(location, totalDistance + distance, visited);
      }
    }

    nextLocations.forEach();

    // for  each route
    return;
  }

  getDistance() {
    return this.getShortestRoute("London", 0, new Set());
  }
}

const locations = new Locations();
console.log("Day 9 part 1:", locations.getDistance());
console.log("Day 9 part 2:");
