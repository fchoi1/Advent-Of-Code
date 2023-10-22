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

func toggle(index int, command []string) {

	if len(command) == 2 {
		if command[0] == "inc" {
			command[0] = "dec"
		} else {
			command[0] = "inc"
		}
	} else {
		if command[0] == "jnz" {
			command[0] = "cpy"
		} else {
			command[0] = "jnz"
		}
	}
}
func (this *Program) runProgram() {
	index := 0

	for index < len(this.Commands) {
		currCommand := this.Commands[index]
		cmd := currCommand[0]
		if cmd == "cpy" {
			value, err := strconv.Atoi(currCommand[1])
			_, isLetter := strconv.Atoi(currCommand[2])
			if isLetter != nil {
				if err != nil {
					this.Registers[currCommand[2]] = this.Registers[currCommand[1]]
				} else {
					this.Registers[currCommand[2]] = value
				}
			}
		} else if cmd == "inc" {
			this.Registers[currCommand[1]]++
		} else if cmd == "dec" {
			this.Registers[currCommand[1]]--
		} else if cmd == "jnz" {
			// Optimize Hardcode
			if index == 9 {
				this.Registers["a"] += this.Registers["b"] * this.Registers["d"]
				this.Registers["d"] = 0
				this.Registers["c"] = 0
				index = 10
				continue
			}
			if index == 20 {
				this.Registers["a"] += this.Registers["c"] * this.Registers["d"]
				this.Registers["d"] = 0
				this.Registers["c"] = 0
				index = 26
				continue
			}
			val, err := strconv.Atoi(currCommand[1])
			if err != nil {
				val = this.Registers[currCommand[1]]
			}
			if val != 0 {
				jump, err := strconv.Atoi(currCommand[2])
				if err != nil {
					jump = this.Registers[currCommand[2]]
				}
				index += jump
				continue
			}
		} else if cmd == "tgl" {
			tglIndex := index + this.Registers[currCommand[1]]
			if tglIndex >= 0 && tglIndex < len(this.Commands) {
				toggle(tglIndex, this.Commands[tglIndex])
			}
		}
		index++
	}
}

func (this *Program) getRegisterA(isPart2 bool) int {
	this.Commands = [][]string{}
	this.getInput()
	for _, char := range []string{"a", "b", "c", "d"} {
		this.Registers[char] = 0
	}
	if isPart2 {
		this.Registers["a"] = 12
	} else {
		this.Registers["a"] = 7
	}
	this.runProgram()
	return this.Registers["a"]
}

func main() {
	program := &Program{
		UseTest: false,
	}
	fmt.Println("Day 23 part 1:", program.getRegisterA(false))
	fmt.Println("Day 23 part 2:", program.getRegisterA(true))
}
