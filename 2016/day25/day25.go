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

func (this *Program) isSignal() bool {
	index, i := 0, 0
	str := ""
	strMatch := strings.Repeat("01", 25)
	for index < len(this.Commands) && i < 200_000 {
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
				i++
				continue
			}
		} else if cmd == "out" {
			val, err := strconv.Atoi(currCommand[1])
			if err != nil {
				val = this.Registers[currCommand[1]]
			}
			str += strconv.Itoa(val)
			if str == strMatch {
				return true
			}
		}
		index++
		i++
	}
	return false
}

func (this *Program) getClockSignal() int {
	i := 0
	for i < 1000 {
		for _, char := range []string{"a", "b", "c", "d"} {
			this.Registers[char] = 0
		}
		this.Registers["a"] = i
		if this.isSignal() {
			return i
		}
		i++
	}
	return -1
}

func main() {
	program := &Program{
		UseTest: false,
	}
	program.getInput()
	fmt.Println("Day 25 part 1:", program.getClockSignal())
}
