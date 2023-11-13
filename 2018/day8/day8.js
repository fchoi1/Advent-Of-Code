const fs = require("fs");

class Node {
  constructor(child, entries) {
    this.children = child;
    this.entries = entries;
    this.childNodes = [];
    this.metaList = [];
    this.meta = 0;
    this.val = 0;
    this.sum = 0;
  }

  addChild(child) {
    this.childNodes.push(child);
    this.sum += child.sum;
  }

  addMeta(val) {
    this.metaList.push(val);
    this.meta += val;
    this.sum += val;
  }
}

class Memory {
  getInput() {
    const inputFile = this.useTest ? "input-test.txt" : "input.txt";
    try {
      const data = fs.readFileSync(inputFile, "utf8").trim().split(/\r?\n/)[0];
      return data.split(" ").map((val) => parseInt(val));
    } catch (err) {
      throw err;
    }
  }

  constructor(useTest = false) {
    this.useTest = useTest;
    this.data = this.getInput();
    this.runList(0, null, 0);
  }

  calculate(node) {
    node.val = node.metaList.reduce((prev, curr) => {
      if (curr > node.childNodes.length) return prev;
      return prev + node.childNodes[curr - 1].val;
    }, 0);
  }

  runList(index, parent) {
    if (index === this.data.length - 1) return index;

    const child = this.data[index];
    const entries = this.data[index + 1];
    const newNode = new Node(child, entries);
    index += 2;

    for (let i = 0; i < child; i++) {
      index = this.runList(index, newNode);
    }

    for (let i = 0; i < entries; i++) {
      newNode.addMeta(this.data[index + i]);
    }

    if (child === 0) newNode.val = newNode.meta;
    else this.calculate(newNode);

    !parent ? (this.rootNode = newNode) : parent.addChild(newNode);

    return index + entries;
  }

  getMetadata() {
    return this.rootNode.sum;
  }

  getRootNode() {
    this.calculate(this.rootNode);
    return this.rootNode.val;
  }
}

const memory = new Memory();
console.log("Day 8 part 1:", memory.getMetadata());
console.log("Day 8 part 2:", memory.getRootNode());
