const fs = require("fs");

class Inventory {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = /\[|\] | /;
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((fabric) => {
        const [date, time, cmd, number] = fabric.split(delimiters).slice(1);
        const action = cmd == "Guard" ? number : cmd;
        return [...date.split("-").map((n) => parseInt(n)), ...time.split(":").map((n) => parseInt(n)), action];
      });
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.timestamps = this.getInput();
    this.guards = {};
    this.longestId = null;
    this.sortTimestamps();
    this.checkGuards();
  }

  sortTimestamps() {
    this.timestamps.sort((a, b) => {
      for (let i = 0; i < 5; i++) {
        if (a[i] !== b[i]) {
          return a[i] > b[i] ? 1 : -1;
        }
      }
      return 0;
    });
  }

  mostOverlapped(numCounts) {
    let mostOverlappedNumber;
    let maxOverlap = 0;
    for (const num in numCounts) {
      if (numCounts[num] > maxOverlap) {
        maxOverlap = numCounts[num];
        mostOverlappedNumber = num;
      }
    }
    return [maxOverlap, mostOverlappedNumber];
  }

  checkGuards() {
    let longest = 0;
    let start, id;
    for (const timestamp of this.timestamps) {
      const action = timestamp[5];
      if (action.includes("#")) {
        id = parseInt(action.slice(1));
      } else if (action === "falls") {
        start = timestamp[4];
      } else if (action === "wakes") {
        if (this.guards[id]) this.guards[id].time += timestamp[4] - start;
        else {
          this.guards[id] = {};
          this.guards[id].time = timestamp[4] - start;
          this.guards[id].numCounts = {};
        }
        for (let i = start; i < timestamp[4]; i++) {
          this.guards[id].numCounts[i] = (this.guards[id].numCounts[i] || 0) + 1;
        }
        if (this.guards[id].time > longest) {
          longest = this.guards[id].time;
          this.longestId = id;
        }
      }
    }
  }

  getGuard() {
    return this.longestId * this.mostOverlapped(this.guards[this.longestId].numCounts)[1];
  }

  getGuardOnMinute() {
    let mostFreq = 0;
    let id, minute;
    for (const guardID in this.guards) {
      const guard = this.guards[guardID];
      if (this.mostOverlapped(guard.numCounts)[0] > mostFreq) {
        id = guardID;
        mostFreq = this.mostOverlapped(guard.numCounts)[0];
        minute = this.mostOverlapped(guard.numCounts)[1];
      }
    }
    return id * minute;
  }
}

const inventory = new Inventory();
console.log("Day 4 part 1:", inventory.getGuard());
console.log("Day 4 part 2:", inventory.getGuardOnMinute());
