package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Elevator struct {
	UseTest    bool
	Elevator   string
	compareBot int
	targetHigh int
	targetLow  int
	targetBot  int
}

func (this *Elevator) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Fields(line)
		fmt.Println(splitted)

	}
	defer file.Close()
}

func (this *Elevator) getMinSteps() int {
	return this.targetBot
}

func main() {
	elevator := &Elevator{
		UseTest: false,
	}
	elevator.getInput()
	fmt.Println("Day 11 part 1:", elevator.getMinSteps())
	// fmt.Println("Day 11 part 2:", Elevator.getProduct())
}
