package main

import (
	"bufio"
	"fmt"
	"os"
)

type Donut struct {
	UseTest bool
	grid    [][]string
	cards   int
}

func (this *Donut) getInput() {
	inputFile := "input.txt"
	this.cards = 10007
	if this.UseTest {
		inputFile = "input-test.txt"
		this.cards = 10
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.grid = [][]string{}

	for scanner.Scan() {
		line := scanner.Text()
		var splitted []string
		for _, char := range line {
			splitted = append(splitted, string(char))
		}
		this.grid = append(this.grid, splitted)
	}

	defer file.Close()
}

func (this *Donut) getSteps() int {
	return 1
}

func main() {
	donut := &Donut{
		UseTest: false,
	}
	donut.getInput()
	fmt.Println("Day 22 part 1:", donut.getSteps())
}
