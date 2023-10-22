package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type HVAC struct {
	UseTest   bool
	Registers map[string]int
	Commands  [][]string
}

func (this *HVAC) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.Registers = make(map[string]int)
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Fields(line)
		this.Commands = append(this.Commands, splitted)
	}
	defer file.Close()
}

func (this *HVAC) getLeastSteps(isPart2 bool) int {
	return 1
}

func main() {
	hvac := &HVAC{
		UseTest: false,
	}
	fmt.Println("Day 24 part 1:", hvac.getLeastSteps(false))
	// fmt.Println("Day 24 part 2:", hvac.getRegisterA(true))
}
