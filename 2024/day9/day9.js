const fs = require("fs");

class Fragmenter {
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
    this.diskmap = this.getInput();
    this.l = this.diskmap.length;
    this.disklength = this.diskmap
      .split("")
      .reduce((a, b) => parseFloat(a) + parseFloat(b));
  }

  sumBetween(start, end) {
    return ((end - start + 1) / 2) * (start + end);
  }

  checksum() {
    let l = 0;
    let r = this.l - 1;
    let i = 0;
    let ans = 0;
    let rFill = 0;
    while (l < r) {
      const leftFill = parseInt(this.diskmap[l]);
      let empty = parseInt(this.diskmap[l + 1]);

      // Fill left
      ans += this.sumBetween(i, i + leftFill - 1) * Math.floor(l / 2);
      i += leftFill;

      // Fill right
      while (empty > 0) {
        if (rFill === 0) rFill = parseInt(this.diskmap[r]);
        const limit = l < r - 2 ? Math.min(empty, rFill) : rFill;

        ans += this.sumBetween(i, i + limit - 1) * Math.floor(r / 2);
        i += limit;

        if (rFill > empty) {
          rFill -= empty;
          empty = 0;
        } else {
          empty -= rFill;
          r -= 2;
          rFill = parseInt(this.diskmap[r]);
        }
      }
      l += 2;
    }
    return ans;
  }

  searchAndReplace(arr, targetRepeat, targetId, maxIndex) {
    let index = 0;
    for (let i = 0; i < arr.length; i++) {
      const [times, id] = arr[i];
      index += times;

      if (id !== ".") continue;
      if (times == targetRepeat) {
        arr[i] = [times, targetId];
        return true;
      } else if (times > targetRepeat) {
        arr.splice(i, 1, [targetRepeat, targetId], [times - targetRepeat, "."]);
        return true;
      }

      if (index >= maxIndex) return false;
    }
    return false;
  }

  checksum2() {
    let loc = [];
    let length = 0;
    for (let i = 0; i < this.l; i += 2) {
      length += parseInt(this.diskmap[i]);
      loc.push([parseInt(this.diskmap[i]), Math.floor(i / 2)]);
      if (i + 1 < this.l) {
        loc.push([parseInt(this.diskmap[i + 1]), "."]);
        length += parseInt(this.diskmap[i + 1]);
      }
    }

    let final = structuredClone(loc);
    let index = length - 1;
    let sub = 0;

    for (let i = loc.length - 1; i >= 0; i--) {
      const [times, id] = loc[i];
      index -= times;
      if (id === ".") continue;
      if (this.searchAndReplace(final, times, id, index)) {
        sub += this.sumBetween(index + 1, index + times) * id;
      }
    }

    let ans = 0;
    let i = 0;
    for (const [times, id] of final) {
      i += times;
      if (id == ".") continue;
      ans += this.sumBetween(i - times, i - 1) * id;
    }

    return ans - sub;
  }
}

const fragmenter = new Fragmenter();
console.log("Day 9 part 1:", fragmenter.checksum());
console.log("Day 9 part 2:", fragmenter.checksum2());
// Total Runtime ~0.55s
