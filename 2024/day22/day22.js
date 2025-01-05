const fs = require("fs");

class MonkeyMarket {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/);
      return data.map((x) => parseInt(x));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.mod = 16777216;
    this.secrets = this.getInput();
  }

  mixPrune(a, b) {
    return (a ^ b) & (this.mod - 1);
  }

  getNext(secret) {
    secret = this.mixPrune(secret, secret << 6);
    secret = this.mixPrune(secret, secret >> 5);
    secret = this.mixPrune(secret, secret << 11);
    return secret;
  }

  combineMaps(m1, m2) {
    const combined = new Map();
    for (let [k, v] of m1) combined.set(k, v);

    for (let [k, v] of m2)
      combined.set(k, v + (combined.has(k) ? combined.get(k) : 0));
    return combined;
  }

  getSecret() {
    let ans = 0;
    const loops = 2000;
    for (let n of this.secrets) {
      for (let i = 0; i < loops; i++) n = this.getNext(n);
      ans += n;
    }
    return ans;
  }

  getMax() {
    const loops = 2000;
    let combined = new Map();

    for (let n of this.secrets) {
      let prevDigit = n % 10;
      let s = "";
      const bananas = new Map();

      for (let i = 0; i < loops; i++) {
        n = this.getNext(n);
        let digit = n % 10;
        let diff = digit - prevDigit;
        prevDigit = digit;

        s += (diff >= 0 ? "+" : "") + String(diff);

        if (i < 3) continue;
        if (i > 3) s = s.slice(2);
        if (bananas.has(s)) continue;
        bananas.set(s, digit);
      }
      combined = this.combineMaps(combined, bananas);
    }
    let maxBananas = 0;
    for (let [_, v] of combined) {
      if (v > maxBananas) maxBananas = v;
    }
    return maxBananas;
  }
}

const monkeyMarket = new MonkeyMarket();
console.log("Day 22 part 1:", monkeyMarket.getSecret());
console.log("Day 22 part 2:", monkeyMarket.getMax());
// Total Runtime ~6s
