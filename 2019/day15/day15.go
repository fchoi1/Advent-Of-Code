package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type GameMap struct {
	UseTest      bool
	IntCode      []int
	relativeBase int
	grid         map[string]rune
}
type Program struct {
	IntCode []int
}

func (this *GameMap) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.IntCode = []int{}
	this.relativeBase = 0
	for scanner.Scan() {
		line := scanner.Text()
		strNum := strings.Split(line, ",")
		for _, n := range strNum {
			num, _ := strconv.Atoi(n)
			this.IntCode = append(this.IntCode, num)
		}
		// additional space need
		for i := 0; i < 15; i++ {
			this.IntCode = append(this.IntCode, 0)
		}
	}
	defer file.Close()
}
func (this *GameMap) parseOpCode(n int) (int, []int) {
	code := n % 100
	rest := strconv.Itoa(n / 100)
	arr := []int{}
	for i := len(rest) - 1; i >= 0; i-- {
		intValue, _ := strconv.Atoi(string(rest[i]))
		arr = append(arr, intValue)
	}
	for len(arr) < 3 {
		arr = append(arr, 0)
	}
	return code, arr
}

func (this *GameMap) runProgram(index int, intCode []int, input []int) ([]int, int) {
	output := []int{}

	for index < len(intCode) {
		code, params := this.parseOpCode(intCode[index])
		if code == 99 {
			return output, -1
		}

		a, b, c := intCode[index+1], intCode[index+2], intCode[index+3]

		if params[0] == 0 {
			a = intCode[a]
		} else if params[0] == 2 {
			a = intCode[a+this.relativeBase]
		}

		switch code {
		case 3, 4:
			if code == 3 {
				if len(input) == 0 {
					return output, index
				}
				if params[0] == 2 {
					intCode[intCode[index+1]+this.relativeBase] = input[0]
				} else {
					intCode[intCode[index+1]] = input[0]
				}
				input = input[1:]
			} else if code == 4 {
				output = append(output, a)
			}
			index += 2
			continue
		case 9:
			this.relativeBase += a
			index += 2
			continue
		}

		if params[1] == 0 {
			b = intCode[b]
		} else if params[1] == 2 {
			b = intCode[b+this.relativeBase]
		}

		if params[2] == 2 {
			c += this.relativeBase
		}
		switch code {
		case 1:
			intCode[c] = a + b
		case 2:
			intCode[c] = a * b
		case 5, 6:
			if (code == 5 && a != 0) || (code == 6 && a == 0) {
				index = b
			} else {
				index += 3
			}
			continue
		case 7, 8:
			intCode[c] = 0
			if (code == 7 && a < b) || (code == 8 && a == b) {
				intCode[c] = 1
			} else {
				intCode[c] = 0
			}
		}
		index += 4
	}
	return output, -1
}

func (this *GameMap) countPanels() int {
	this.getInput()
	fmt.Println(len(this.IntCode))
	return 1
}

func (this *GameMap) bfs() int {
	coordMap := make(map[string]Program)
	fmt.Println(coordMap)
	return 1
}

// func (this *GameMap) getScore() int {
// 	this.getInput()
// 	return 1
// }

func main() {
	gameMap := &GameMap{
		UseTest: false,
		IntCode: []int{},
	}
	fmt.Println("Day 15 part 1:", gameMap.countPanels())
	// fmt.Println("Day 13 part 2:", gameMap.getScore())
}
