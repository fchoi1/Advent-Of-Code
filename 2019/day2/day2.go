package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Alarm struct {
	UseTest bool
	IntCode []int
}

func (this *Alarm) getInput() {
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

func (this *Alarm) runProgram(input1 int, input2 int) int {
	this.getInput()
	index := 0
	this.IntCode[1] = input1
	this.IntCode[2] = input2

	for index < len(this.IntCode) {
		code := this.IntCode[index]
		var res int
		a := this.IntCode[index+1]
		b := this.IntCode[index+2]
		c := this.IntCode[index+3]
		if code == 99 {
			return this.IntCode[0]
		} else if code == 1 {
			res = this.IntCode[a] + this.IntCode[b]
		} else if code == 2 {
			res = this.IntCode[a] * this.IntCode[b]
		}
		this.IntCode[c] = res
		index += 4
	}
	return this.IntCode[0]
}

func (this *Alarm) getOutput() int {
	return this.runProgram(12, 2)
}

func (this *Alarm) getOutput2() int {
	target := 19690720
	for i := 0; i < 100; i++ {
		for j := 0; j < 100; j++ {
			if target == this.runProgram(i, j) {
				return 100*i + j
			}
		}
	}
	return -1
}

func main() {
	alarm := &Alarm{
		UseTest: false,
		IntCode: []int{},
	}
	fmt.Println("Day 2 part 1:", alarm.getOutput())
	fmt.Println("Day 2 part 2:", alarm.getOutput2())
}
