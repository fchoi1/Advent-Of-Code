const fs = require("fs");

class Reindeer {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    const delimiters = / can fly | km\/s for | seconds, but then must rest for |seconds\./;
    try {
      const reindeers = {};
      const data = fs.readFileSync(inputFile, "utf8").trim().split("\r\n");
      data.forEach((rule) => {
        const [reindeer, speed, speedTime, restTime] = rule.split(delimiters);
        reindeers[reindeer] = reindeers[reindeer] || {};
        reindeers[reindeer] = {
          speed: parseInt(speed),
          speedTime: parseInt(speedTime),
          restTime: parseInt(restTime),
          total: parseInt(speedTime) + parseInt(restTime),
          distance: 0,
          points: 0,
        };
      });
      return reindeers;
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.reindeers = this.getInput();
    this.time = useTest ? 1000 : 2500;
    console.log(this.reindeers);
  }

  getDistance() {
    let maxDist = 0;

    for (const reindeer of Object.values(this.reindeers)) {
      let distance = Math.floor(this.time / reindeer.total) * reindeer.speed * reindeer.speedTime;
      const remainTime = Math.min(this.time % reindeer.total, reindeer.speedTime);
      distance += remainTime * reindeer.speed;
      maxDist = Math.max(maxDist, distance);
    }
    return maxDist;
  }

  getNewtDistance() {
    for (let i = 0; i < this.time; i++) {
      let currentDist = 0;
      const furthest = Object.entries(this.reindeers).reduce((acc, [name, reindeer]) => {
        if (i % reindeer.total < reindeer.speedTime) {
          this.reindeers[name].distance += reindeer.speed;
        }

        if (this.reindeers[name].distance > currentDist) {
          acc = [name];
          currentDist = this.reindeers[name].distance;
        } else if (this.reindeers[name].distance === currentDist) {
          acc.push(name);
        }
        return acc;
      }, []);

      furthest.forEach((reindeer) => {
        this.reindeers[reindeer].points += 1;
      });
    }
    return Math.max(...Object.values(this.reindeers).map((reindeer) => reindeer.points));
  }
}

const reindeer = new Reindeer();
console.log("Day 14 part 1:", reindeer.getDistance());
console.log("Day 14 part 2:", reindeer.getNewtDistance());
