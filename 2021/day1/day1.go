package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Sonar struct {
	useTest bool
	report  []int
}

func (this *Sonar) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-text.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		val, _ := strconv.Atoi(line)
		this.report = append(this.report, val)
	}
	defer file.Close()
}

func (this *Sonar) getLarger(window int) int {
	var larger, prev int
	for i := 0; i < window; i++ {
		prev += this.report[i]
	}
	for index, val := range this.report[window:] {
		curr := prev - this.report[index] + val
		if curr > prev {
			larger++
		}
		prev = curr
	}
	return larger
}

func main() {
	sonar := &Sonar{
		useTest: false,
	}
	sonar.getInput()
	fmt.Println("Day 1 part 1:", sonar.getLarger(1))
	fmt.Println("Day 1 part 2:", sonar.getLarger(3))
}
