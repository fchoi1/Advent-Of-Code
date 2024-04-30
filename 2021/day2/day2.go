package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Command struct {
	movement string
	steps    int
}

type Dive struct {
	useTest  bool
	commands []Command
}

func (this *Dive) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-text.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		cmd := strings.Fields(line)
		steps, _ := strconv.Atoi(cmd[1])
		this.commands = append(this.commands, Command{cmd[0], steps})
	}
	defer file.Close()
}

func (this *Dive) getLocation() int {
	var depth, horizontal int
	for _, cmd := range this.commands {
		if cmd.movement == "forward" {
			horizontal += cmd.steps
		} else if cmd.movement == "down" {
			depth += cmd.steps
		} else if cmd.movement == "up" {
			depth -= cmd.steps
		}
	}
	return horizontal * depth
}

func (this *Dive) getLocationAim() int {
	var depth, horizontal, aim int
	for _, cmd := range this.commands {
		if cmd.movement == "forward" {
			horizontal += cmd.steps
			depth += aim * cmd.steps
		} else if cmd.movement == "down" {
			aim += cmd.steps
		} else if cmd.movement == "up" {
			aim -= cmd.steps
		}
	}
	return horizontal * depth
}

func main() {
	dive := &Dive{
		useTest: false,
	}
	dive.getInput()
	fmt.Println("Day 2 part 1:", dive.getLocation())
	fmt.Println("Day 2 part 2:", dive.getLocationAim())
}
