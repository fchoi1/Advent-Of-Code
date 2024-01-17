package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Amplifier struct {
	UseTest   bool
	IntCode   []int
	comboList [][]int
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func contains(slice []int, value int) bool {
	for _, v := range slice {
		if v == value {
			return true
		}
	}
	return false
}

func (this *Amplifier) getInput() {
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
func (this *Amplifier) parseOpCode(n int) (int, []int) {
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

func (this *Amplifier) runProgram(index int, intCode []int, input []int) ([]int, int) {
	output := []int{}
	for index < len(intCode) {
		code, params := this.parseOpCode(intCode[index])
		if code == 99 {
			return output, -1
		}
		a := intCode[index+1]
		switch code {
		case 3, 4:
			if code == 3 {
				if len(input) == 0 {
					return output, index
				}
				intCode[a] = input[0]
				input = input[1:]

			} else if code == 4 {
				output = append(output, intCode[a])
			}
			index += 2
			continue
		}
		b, c := intCode[index+2], intCode[index+3]
		if params[0] == 0 {
			a = intCode[a]
		}
		if params[1] == 0 {
			b = intCode[b]
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

func backtrack(values []int, currCombo []int, result *[][]int) {
	if len(currCombo) == 5 {
		*result = append(*result, append([]int{}, currCombo...))
		return
	}

	for _, v := range values {
		if contains(currCombo, v) {
			continue
		}
		currCombo = append(currCombo, v)
		backtrack(values, currCombo, result)
		currCombo = currCombo[:len(currCombo)-1]
	}
}

func (this *Amplifier) getCombo(values []int) [][]int {
	var res [][]int
	backtrack(values, []int{}, &res)
	return res
}

func (this *Amplifier) getOutput(isPart2 bool) int {
	var comboList [][]int
	var outputs []int
	nextIndex := [5]int{0, 0, 0, 0, 0}
	inputList := make([][]int, 5)
	codeList := make([][]int, 5)
	maxOuput := 0

	if !isPart2 {
		comboList = this.getCombo([]int{0, 1, 2, 3, 4})
	} else {
		comboList = this.getCombo([]int{5, 6, 7, 8, 9})
	}

	for _, combo := range comboList {

		for i := 0; i < 5; i++ {
			inputList[i] = append([]int{}, combo[i])
			if i == 0 {
				inputList[i] = append(inputList[i], 0)
			}
			codeList[i] = append([]int{}, this.IntCode...)
			nextIndex[i] = 0
		}
	outerLoop:
		for {
			for i := 0; i < 5; i++ {
				if nextIndex[i] == -1 {
					continue
				}
				outputs, nextIndex[i] = this.runProgram(nextIndex[i], codeList[i], inputList[i])
				if nextIndex[4] == -1 {
					break outerLoop
				}
				inputList[i] = []int{}
				inputList[(i+1)%5] = append(inputList[(i+1)%5], outputs...)
			}
		}
		maxOuput = max(maxOuput, outputs[0])
	}
	return maxOuput
}

func main() {
	amplifier := &Amplifier{
		UseTest: false,
		IntCode: []int{},
	}
	amplifier.getInput()
	fmt.Println("Day 7 part 1:", amplifier.getOutput(false))
	fmt.Println("Day 7 part 2:", amplifier.getOutput(true))

}
