package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Tractor struct {
	UseTest      bool
	IntCode      []int
	relativeBase int
}

func (this *Tractor) getInput() {
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
		for i := 0; i < 30; i++ {
			this.IntCode = append(this.IntCode, 0)
		}
	}
	defer file.Close()
}
func (this *Tractor) parseOpCode(n int) (int, []int) {
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

func (this *Tractor) runProgram(index int, intCode []int, input []int) ([]int, int) {
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

func (this *Tractor) countBeam() int {
	this.relativeBase = 0
	var count int
	for y := 0; y < 50; y++ {
		for x := 0; x < 50; x++ {
			this.getInput()
			out, _ := this.runProgram(0, this.IntCode, []int{x, y})
			if out[0] == 1 {
				count++
			}
		}
	}
	return count
}

func (this *Tractor) findGrid() int {
	x, y := this.search()
	return x*10000 + y
}

func (this *Tractor) search() (int, int) {
	target := 100
	height := 1100
	yStart := 500
	var start int
	var currKey string
	ends := make(map[string]bool)
	for y := yStart; y < height; y++ {
		x := start
		prev := 0
		for true {
			this.getInput()
			out, _ := this.runProgram(0, this.IntCode, []int{x, y})
			if out[0] == 1 {
				if prev == 0 {
					start = x
				}
				strKey := strconv.Itoa(x+target-1) + "," + strconv.Itoa(y-target+1)
				if ends[strKey] {
					return x, y - target + 1
				}
				currKey = strconv.Itoa(x) + "," + strconv.Itoa(y)

			} else if prev == 1 {
				ends[currKey] = true
				break
			}
			prev = out[0]
			x += 1
		}
	}
	return -1, -1
}

func main() {
	tractor := &Tractor{
		UseTest: false,
		IntCode: []int{},
	}
	tractor.getInput()
	fmt.Println("Day 19 part 1:", tractor.countBeam())
	fmt.Println("Day 19 part 2:", tractor.findGrid())
	// Total Runtime ~3.4s
}
