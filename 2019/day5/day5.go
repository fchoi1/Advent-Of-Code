package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Asteroids struct {
	UseTest bool
	IntCode []int
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func (this *Asteroids) getInput() {
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
func (this *Asteroids) parseOpCode(n int) (int, []int) {
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

func (this *Asteroids) runProgram(input int) int {
	index := 0
	var output int
	for index < len(this.IntCode) {
		code, params := this.parseOpCode(this.IntCode[index])
		if code == 99 {
			return output
		}
		a, b, c := this.IntCode[index+1], this.IntCode[index+2], this.IntCode[index+3]

		switch code {
		case 3, 4:
			if code == 3 {
				this.IntCode[a] = input
			} else if code == 4 {
				output = this.IntCode[a]
			}
			index += 2
			continue
		}

		if params[0] == 0 {
			a = this.IntCode[a]
		}
		if params[1] == 0 {
			b = this.IntCode[b]
		}

		switch code {
		case 1:
			this.IntCode[c] = a + b
		case 2:
			this.IntCode[c] = a * b
		case 5, 6:
			if (code == 5 && a != 0) || (code == 6 && a == 0) {
				index = b
			} else {
				index += 3
			}
			continue
		case 7, 8:
			this.IntCode[c] = 0
			if (code == 7 && a < b) || (code == 8 && a == b) {
				this.IntCode[c] = 1
			} else {
				this.IntCode[c] = 0
			}
		}
		index += 4
	}
	return this.IntCode[0]
}

func (this *Asteroids) getOutput(isPart2 bool) int {
	this.getInput()
	in := 1
	if isPart2 {
		in = 5
	}
	return this.runProgram(in)
}

func main() {
	asteroids := &Asteroids{
		UseTest: false,
		IntCode: []int{},
	}
	fmt.Println("Day 5 part 1:", asteroids.getOutput(false))
	fmt.Println("Day 5 part 2:", asteroids.getOutput(true))

}
