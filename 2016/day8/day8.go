package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Screen struct {
	UseTest  bool
	width    int
	height   int
	Screen   [][]string
	Commands []interface{}
	onLights int
}

func makeScreen(height int, width int) [][]string {
	twoDSlice := make([][]string, height)
	for i := range twoDSlice {
		twoDSlice[i] = make([]string, width)
		for j := range twoDSlice[i] {
			twoDSlice[i][j] = "."
		}
	}
	return twoDSlice
}

func (this *Screen) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == ' ' || r == '=' || r == 'x' || r == 'y'
		})
		if splitted[0] == "rect" {
			width, _ := strconv.Atoi(splitted[1])
			height, _ := strconv.Atoi(splitted[2])
			this.Commands = append(this.Commands, []interface{}{splitted[0], width, height})
		} else {
			target, _ := strconv.Atoi(splitted[2])
			shift, _ := strconv.Atoi(splitted[4])
			this.Commands = append(this.Commands, []interface{}{splitted[1], target, shift})
		}
	}
	defer file.Close()
}

func (this *Screen) runCommands() {
	for _, commandInterface := range this.Commands {
		command := commandInterface.([]interface{})
		cmd := command[0].(string)
		int1 := command[1].(int)
		int2 := command[2].(int)
		if cmd == "rect" {
			for j := 0; j < int2; j++ {
				for i := 0; i < int1; i++ {
					this.Screen[j][i] = "#"
				}
			}
		} else if cmd == "column" {
			column := make([]string, len(this.Screen))
			for i, row := range this.Screen {
				column[i] = row[int1]
			}
			shift := int2 % len(this.Screen)
			shiftedColumn := append(column[len(column)-shift:], column[:len(column)-shift]...)

			for i, row := range this.Screen {
				row[int1] = shiftedColumn[i]
			}
		} else if cmd == "row" {
			row := this.Screen[int1]
			shift := int2 % this.width
			this.Screen[int1] = append(row[len(row)-shift:], row[:len(row)-shift]...)
		}
	}
}

func (this *Screen) printScreen() {
	for _, row := range this.Screen {
		fmt.Println(row)
	}
}

func (this *Screen) getOnLights() int {
	count := 0
	for _, row := range this.Screen {
		for _, val := range row {
			if val == "#" {
				count++
			}
		}
	}
	this.onLights = count
	return this.onLights
}

func main() {
	width := 50
	height := 6
	screen := &Screen{
		UseTest: false,
		width:   width,
		height:  height,
		Screen:  makeScreen(height, width),
	}
	screen.getInput()
	screen.runCommands()
	fmt.Println("Day 8 part 1:", screen.getOnLights())
	fmt.Println("Day 8 part 2:")
	screen.printScreen()
}
