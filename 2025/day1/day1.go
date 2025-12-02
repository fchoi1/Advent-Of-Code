package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

type Dial struct {
	useTest   bool
	rotations []string
	start     int
	zeros     int
	crosses   int
}

func mod(a, b int) int {
	return (a%b + b) % b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func (this *Dial) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.rotations = append(this.rotations, line)
	}
	defer file.Close()
}

func (this *Dial) rotate() {
	this.zeros = 0
	this.crosses = 0
	for _, val := range this.rotations {
		dir := rune(val[0])
		value, _ := strconv.Atoi(val[1:])

		this.crosses += max(value/100, 0)
		remain := mod(value, 100)
		prev := this.start
		if dir == 'L' {
			this.start -= remain
		} else if dir == 'R' {
			this.start += remain
		}

		// Prevent double count when land on 0
		if (prev != 0) && this.start != mod(this.start, 100) || this.start == 0 {
			this.crosses++
		}

		this.start = mod(this.start, 100)
		if this.start == 0 {
			this.zeros++
		}
	}
}

func (this *Dial) getZeros() int {
	return this.zeros
}

func (this *Dial) getCrosses() int {
	return this.crosses
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()

	dial := &Dial{
		useTest: *useTest,
		start:   50,
	}
	dial.getInput()
	dial.rotate()
	fmt.Println("Day 1 part 1:", dial.getZeros())
	fmt.Println("Day 1 part 1:", dial.getCrosses())
}
