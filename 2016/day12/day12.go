package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Program struct {
	UseTest   bool
	Registers map[string]int
	Commands  [][]string
}

func (this *Program) getInput() {
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

func (this *Program) runProgram() {
	index := 0
	for index < len(this.Commands) {
		currCommand := this.Commands[index]
		cmd := currCommand[0]
		if cmd == "cpy" {
			value, err := strconv.Atoi(currCommand[1])
			if err != nil {
				this.Registers[currCommand[2]] = this.Registers[currCommand[1]]
			} else {
				this.Registers[currCommand[2]] = value
			}
		} else if cmd == "inc" {
			this.Registers[currCommand[1]]++
		} else if cmd == "dec" {
			this.Registers[currCommand[1]]--
		} else if cmd == "jnz" {
			val, err := strconv.Atoi(currCommand[1])
			if err != nil {
				val = this.Registers[currCommand[1]]
			}
			if val != 0 {
				jump, _ := strconv.Atoi(currCommand[2])
				index += jump
				continue
			}
		}
		index++
	}
}

func (this *Program) getRegisterA(isPart2 bool) int {
	for _, char := range []string{"a", "b", "c", "d"} {
		this.Registers[char] = 0
	}
	if isPart2 {
		this.Registers["c"] = 1
	}
	this.runProgram()
	return this.Registers["a"]
}

func main() {
	program := &Program{
		UseTest: false,
	}
	program.getInput()
	fmt.Println("Day 12 part 1:", program.getRegisterA(false))
	fmt.Println("Day 12 part 2:", program.getRegisterA(true))
}
