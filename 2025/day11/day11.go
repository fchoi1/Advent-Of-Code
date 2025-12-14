package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
)

type Reactor struct {
	useTest  bool
	part1    int
	part2    int
	cables   []Node
	cableMap map[string][]string
}

type Node struct {
	val     string
	outputs []string
}

func (this *Reactor) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, ": ")
		input := parts[0]
		outputLst := strings.Split(parts[1], " ")

		node := Node{val: input}
		for _, output := range outputLst {
			node.outputs = append(node.outputs, output)
		}
		this.cables = append(this.cables, node)
	}
	this.buildMap()
	defer file.Close()
}

func (this *Reactor) buildMap() {
	this.cableMap = make(map[string][]string)
	for _, cable := range this.cables {
		this.cableMap[cable.val] = cable.outputs
	}
}

func (this *Reactor) countPaths(start, target string) int {
	memo := make(map[string]int)

	var dfs func(node string) int
	// With memo
	dfs = func(node string) int {
		if node == target {
			return 1
		}
		if val, ok := memo[node]; ok {
			return val
		}

		total := 0
		for _, next := range this.cableMap[node] {
			total += dfs(next)
		}

		memo[node] = total
		return total
	}

	return dfs(start)
}
func (this *Reactor) getPart1() int {
	return this.countPaths("you", "out")
}

func (this *Reactor) getPart2() int {

	// Since it is a dag, the reverse is not possible
	svr2fft := this.countPaths("svr", "fft")
	fft2dac := this.countPaths("fft", "dac")
	dac2out := this.countPaths("dac", "out")

	return svr2fft * fft2dac * dac2out
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()
	reactor := &Reactor{
		useTest: *useTest,
	}
	reactor.getInput()
	fmt.Println("Day 11 part 1:", reactor.getPart1())
	fmt.Println("Day 11 part 2:", reactor.getPart2())
}
