package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type TrashCompactor struct {
	useTest bool
	numbers [][]int
	ops     []string
	numStr  []string
	opsStr  string
}

func (this *TrashCompactor) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		nums := strings.Fields(line)

		var numList []int

		if nums[0] != "*" && nums[0] != "+" {
			for _, val := range nums {
				converted, _ := strconv.Atoi(val)
				numList = append(numList, converted)
			}
			this.numbers = append(this.numbers, numList)
			this.numStr = append(this.numStr, line+" ")
		} else {
			this.ops = nums
			this.opsStr = line + " "
		}

	}
	defer file.Close()
}

func (this *TrashCompactor) calculate() int {
	var result []int
	for _, op := range this.ops {
		if op == "*" {
			result = append(result, 1)
		} else {
			result = append(result, 0)
		}
	}

	for _, row := range this.numbers {
		for i, val := range row {
			op := this.ops[i]
			if op == "*" {
				result[i] *= val
			} else {
				result[i] += val
			}
		}
	}

	var ans int
	for _, n := range result {
		ans += n
	}
	return ans
}

func (this *TrashCompactor) calculateCol() int {
	var ans int
	var currOp rune
	var currAns int

	N := len(this.numStr)
	for i, opVal := range this.opsStr {

		// get num per col
		var numStr string
		for j := 0; j < N; j++ {
			if this.numStr[j][i] == ' ' {
				continue
			} else {
				numStr += string(this.numStr[j][i])
			}
		}
		if numStr == "" {
			ans += currAns
			continue
		}

		currNum, _ := strconv.Atoi(numStr)
		if opVal == '+' || opVal == '*' {
			currOp = opVal
			currAns = currNum
		} else {
			if currOp == '*' {
				currAns *= currNum
			} else {
				currAns += currNum
			}
		}
	}
	return ans

}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()
	trashCompactor := &TrashCompactor{
		useTest: *useTest,
	}
	trashCompactor.getInput()
	fmt.Println("Day 6 part 1:", trashCompactor.calculate())
	fmt.Println("Day 6 part 2:", trashCompactor.calculateCol())
}
