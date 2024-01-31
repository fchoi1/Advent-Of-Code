package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type PaintMap struct {
	UseTest      bool
	IntCode      []int
	relativeBase int
	maxRange     []int
	minRange     []int
	count        int
	white        map[string]bool
}

func mod(a, b int) int {
	return (a%b + b) % b
}

func (this *PaintMap) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.IntCode = []int{}
	for scanner.Scan() {
		line := scanner.Text()
		strNum := strings.Split(line, ",")
		for _, n := range strNum {
			num, _ := strconv.Atoi(n)
			this.IntCode = append(this.IntCode, num)
		}
	}
	this.white = make(map[string]bool)
	this.maxRange = []int{0, 0}
	this.minRange = []int{0, 0}
	for i := 0; i < 450; i++ {
		this.IntCode = append(this.IntCode, 0)
	}
	defer file.Close()
}
func (this *PaintMap) parseOpCode(n int) (int, []int) {
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

func (this *PaintMap) runProgram(index int, intCode []int, input []int) ([]int, int) {
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

func (this *PaintMap) paintRobot(initialInput int) {
	input, nextIndex, direction := initialInput, 0, 0
	location := []int{0, 0}
	dirMap := [][]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}
	black := make(map[string]bool)
	var out []int
	strKey := "0,0"
	for nextIndex != -1 {
		for i := 0; i < 2; i++ {
			if location[i] > this.maxRange[i] {
				this.maxRange[i] = location[i]
			}
			if location[i] < this.minRange[i] {
				this.minRange[i] = location[i]
			}
		}
		out, nextIndex = this.runProgram(nextIndex, this.IntCode, []int{input})
		_, blackExists := black[strKey]
		_, whiteExists := this.white[strKey]
		if !blackExists && !whiteExists {
			this.count++
		}
		if out[0] == 0 {
			black[strKey] = true
			delete(this.white, strKey)
		} else {
			this.white[strKey] = true
			delete(black, strKey)
		}
		if out[1] == 1 {
			direction = mod(direction+1, 4)
		} else {
			direction = mod(direction-1, 4)
		}
		location[0] += dirMap[direction][0]
		location[1] += dirMap[direction][1]
		strKey = strconv.Itoa(location[0]) + "," + strconv.Itoa(location[1])
		if this.white[strKey] {
			input = 1
		} else {
			input = 0
		}
	}
}

func (this *PaintMap) countPanels() int {
	this.getInput()
	this.paintRobot(0)
	return this.count
}

func (this *PaintMap) printPanels() {
	this.getInput()
	this.paintRobot(1)
	for y := this.minRange[1]; y <= this.maxRange[1]; y++ {
		for x := this.minRange[0]; x < this.maxRange[0]; x++ {
			strKey := strconv.Itoa(x) + "," + strconv.Itoa(y)
			if this.white[strKey] {
				fmt.Print("# ")
			} else {
				fmt.Print(". ")
			}
		}
		fmt.Println()
	}
}

func main() {
	paintMap := &PaintMap{
		UseTest: false,
		IntCode: []int{},
	}
	paintMap.getInput()
	fmt.Println("Day 11 part 1:", paintMap.countPanels())
	fmt.Println("Day 11 part 2:")
	paintMap.printPanels()
}
