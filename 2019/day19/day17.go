package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Scaffolding struct {
	UseTest      bool
	IntCode      []int
	relativeBase int
	alignment    int
	start        [2]int
	grid         [][]string
	dust         int
}

func (this *Scaffolding) getInput() {
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
		// additional space needed
		for i := 0; i < 8000; i++ {
			this.IntCode = append(this.IntCode, 0)
		}
	}
	defer file.Close()
}
func (this *Scaffolding) parseOpCode(n int) (int, []int) {
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

func (this *Scaffolding) runProgram(index int, intCode []int, input []int) ([]int, int) {
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

func (this *Scaffolding) calculate() int {
	this.parseMap()
	for y := 0; y < len(this.grid)-1; y++ {
		for x := 0; x < len(this.grid[0]); x++ {
			if strings.ContainsRune("<>^v", []rune(this.grid[y][x])[0]) {
				this.start = [2]int{x, y}
			}

			if y == 0 || x == 0 || y >= len(this.grid)-2 || x >= len(this.grid[0])-1 {
				continue
			}
			if this.grid[y][x] == "#" {
				if this.grid[y-1][x] == "#" && this.grid[y+1][x] == "#" && this.grid[y][x+1] == "#" && this.grid[y][x-1] == "#" {
					this.alignment += (y * x)
				}
			}
		}
	}
	this.getInstructions()
	return this.alignment
}

func (this *Scaffolding) getInstructions() {
	dirMap := [][]int{
		{0, -1}, {1, 0}, {0, 1}, {-1, 0},
	}
	dirStr := "L"
	direction := 3
	commandStr := ""

	pos := this.start
	var newX, newY, count int
	var check bool

	for {
		check = true
		newX, newY = dirMap[direction][0]+pos[0], dirMap[direction][1]+pos[1]
		if newX >= 0 && newX < len(this.grid[0]) && newY >= 0 && newY < len(this.grid)-1 {
			if this.grid[newY][newX] == "#" {
				pos[0] = newX
				pos[1] = newY
				count += 1
				check = false
			}
		}

		if check {
			commandStr += dirStr + strconv.Itoa(count) + " "
			count = 0
			left := dirMap[(direction+4-1)%4]
			right := dirMap[(direction+1)%4]

			leftX, leftY := left[0]+pos[0], left[1]+pos[1]
			rightX, rightY := right[0]+pos[0], right[1]+pos[1]

			if this.grid[leftY][leftX] == "#" {
				direction = (direction + 4 - 1) % 4
				dirStr = "L"
			} else if this.grid[rightY][rightX] == "#" {
				direction = (direction + 1) % 4
				dirStr = "R"
			} else {
				break
			}
		}
	}
	// fmt.Println(commandStr)
	//(L12 R8 L6 R8 L6) [R8 L12 L12 R8] (L12 R8 L6 R8 L6) (L12 R8 L6 R8 L6 )[R8 L12 L12 R8] {L6 R6 L12} [R8 L12 L12 R8] {L6 R6 L12} {L6 R6 L12} [R8 L12 L12 R8]
	this.getInput()
	this.IntCode[0] = 2
	routine := this.getAscii("A,B,A,A,B,C,B,C,C,B\n")
	A := this.getAscii("L,12,R,8,L,6,R,8,L,6\n")
	B := this.getAscii("R,8,L,12,L,12,R,8\n")
	C := this.getAscii("L,6,R,6,L,12\n")
	ans := this.getAscii("n\n")
	_, nextIndex := this.runProgram(0, this.IntCode, routine)
	_, nextIndex = this.runProgram(nextIndex, this.IntCode, A)
	_, nextIndex = this.runProgram(nextIndex, this.IntCode, B)
	_, nextIndex = this.runProgram(nextIndex, this.IntCode, C)
	out, _ := this.runProgram(nextIndex, this.IntCode, ans)
	this.dust = out[len(out)-1]
}

func (this *Scaffolding) getAscii(str string) []int {
	asciiValues := []int{}
	for _, char := range str {
		asciiValues = append(asciiValues, int(char))
	}
	return asciiValues
}

func (this *Scaffolding) parseMap() [][]string {
	this.getInput()
	output, _ := this.runProgram(0, this.IntCode, []int{})
	row := []string{}
	for _, num := range output {
		if num == 10 {
			this.grid = append(this.grid, row)
			// fmt.Println(row)
			row = []string{}
			continue
		}
		row = append(row, string(num))
	}
	return this.grid
}

func (this *Scaffolding) getAlignment() int {
	return this.alignment
}
func (this *Scaffolding) getDust() int {
	return this.dust
}

func main() {
	scaffolding := &Scaffolding{
		UseTest: false,
		IntCode: []int{},
	}
	scaffolding.calculate()
	fmt.Println("Day 17 part 1:", scaffolding.getAlignment())
	fmt.Println("Day 17 part 2:", scaffolding.getDust())
}
