package main

import (
	"bufio"
	"fmt"
	"os"
)

type Robot struct {
	UseTest bool
	grid    [][]string
}

func (this *Robot) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
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

func (this *Robot) getSteps() int {
	for _, row := range this.grid {
		fmt.Println(row)
	}
	return 1
}

func main() {
	robot := &Robot{
		UseTest: false,
	}
	robot.getInput()
	fmt.Println("Day 20 part 1:", robot.getSteps())

}
