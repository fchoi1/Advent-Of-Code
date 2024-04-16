package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type OxygenSystem struct {
	UseTest    bool
	IntCode    []int
	grid       [][]rune
	minSteps   int
	oxygen     []int
	oxygenTime int
}
type Node struct {
	IntCode      []int
	x            int
	y            int
	relativeBase int
	index        int
	key          string
}

func (this *OxygenSystem) getInput() {
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
	defer file.Close()
}
func (this *OxygenSystem) parseOpCode(n int) (int, []int) {
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

func (this *OxygenSystem) runProgram(index int, relativeBase int, intCode []int, input []int) ([]int, int, int) {
	output := []int{}

	for index < len(intCode) {
		code, params := this.parseOpCode(intCode[index])
		if code == 99 {
			return output, -1, relativeBase
		}

		a, b, c := intCode[index+1], intCode[index+2], intCode[index+3]

		if params[0] == 0 {
			a = intCode[a]
		} else if params[0] == 2 {
			a = intCode[a+relativeBase]
		}

		switch code {
		case 3, 4:
			if code == 3 {
				if len(input) == 0 {
					return output, index, relativeBase
				}
				if params[0] == 2 {
					intCode[intCode[index+1]+relativeBase] = input[0]
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
			relativeBase += a
			index += 2
			continue
		}

		if params[1] == 0 {
			b = intCode[b]
		} else if params[1] == 2 {
			b = intCode[b+relativeBase]
		}

		if params[2] == 2 {
			c += relativeBase
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
	return output, -1, relativeBase
}

func (this *OxygenSystem) fillOxygen() {

	q := [][]int{this.oxygen}
	this.grid[this.oxygen[1]][this.oxygen[0]] = '.'
	var steps int
	for len(q) > 0 {
		temp := [][]int{}
		for _, node := range q {
			x, y := node[0], node[1]
			if this.grid[y][x] != '.' {
				continue
			}
			this.grid[y][x] = 'O'
			for _, dir := range [][]int{{0, -1}, {0, 1}, {1, 0}, {-1, 0}} {
				temp = append(temp, []int{x + dir[0], y + dir[1]})
			}
		}
		q = temp
		if len(q) == 0 {
			break
		}
		steps++
	}
	this.oxygenTime = steps - 1
}

func (this *OxygenSystem) makeGrid() {
	length := 45
	this.grid = make([][]rune, length)
	for i := range this.grid {
		this.grid[i] = make([]rune, length)
		for j := range this.grid[i] {
			this.grid[i][j] = '#'
		}
	}
	dirMap := [][]int{{0, -1}, {0, 1}, {1, 0}, {-1, 0}}
	intCode := make([]int, len(this.IntCode))
	copy(intCode, this.IntCode)

	q := []Node{{intCode, length / 2, length / 2, 0, 0, strconv.Itoa(length/2) + "," + strconv.Itoa(length/2)}}
	seen := make(map[string]bool)

	var steps int
	for len(q) > 0 && steps < 1000 {
		temp := []Node{}
		for _, node := range q {
			seen[node.key] = true

			for _, dir := range []int{1, 2, 3, 4} {

				relBase := node.relativeBase
				intCode := make([]int, len(node.IntCode))
				copy(intCode, node.IntCode)
				index := node.index

				out, index, relBase := this.runProgram(index, relBase, intCode, []int{dir})

				x := node.x + dirMap[dir-1][0]
				y := node.y + dirMap[dir-1][1]
				key := strconv.Itoa(x) + "," + strconv.Itoa(y)

				if out[0] == 2 {
					this.grid[y][x] = 'X'
					if this.minSteps == 0 {
						this.oxygen = []int{x, y}
						this.minSteps = steps + 1
					}
				} else if out[0] == 1 {
					this.grid[y][x] = '.'
					if _, ok := seen[key]; ok {
						continue
					}
					temp = append(temp, Node{intCode, x, y, relBase, index, key})
				} else {
					this.grid[y][x] = '#'
				}
			}
		}
		q = temp
		steps++
	}
}

func (this *OxygenSystem) runSystem() {
	this.getInput()
	this.makeGrid()
	this.fillOxygen()
}

func (this *OxygenSystem) findOxygen() int {
	return this.minSteps
}

func (this *OxygenSystem) runOxygen() int {
	return this.oxygenTime
}

func main() {
	oxygenSystem := &OxygenSystem{
		UseTest: false,
	}
	oxygenSystem.runSystem()
	fmt.Println("Day 15 part 1:", oxygenSystem.findOxygen())
	fmt.Println("Day 15 part 2:", oxygenSystem.runOxygen())
}
