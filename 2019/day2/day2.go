package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Rocket struct {
	UseTest bool
	IntCode []int
}

func (this *Rocket) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
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

func (this *Rocket) getFuel() int {
	total := 0
	index := 0

	for index < len(this.IntCode)-3 {
		code := this.IntCode[index]
		var res int
		a := this.IntCode[index+1]
		b := this.IntCode[index+2]
		c := this.IntCode[index+3]
		fmt.Println(a, b, c)
		if code == 99 {
			fmt.Println("broke", code, a, b, c)
			return 1
		} else if code == 1 {
			res = this.IntCode[a] + this.IntCode[b]
		} else if code == 2 {
			res = this.IntCode[a] * this.IntCode[b]
		}
		this.IntCode[c] = res
		fmt.Println(res, index, this.IntCode)
		index += 4

	}
	fmt.Println((this.IntCode))
	return total
}

func main() {
	rocket := &Rocket{
		UseTest: true,
		IntCode: []int{},
	}
	rocket.getInput()
	fmt.Println("Day 1 part 1:", rocket.getFuel())
	fmt.Println("Day 1 part 2:", rocket.getFuel())
}
