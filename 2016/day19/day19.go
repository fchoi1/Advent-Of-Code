package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
)

type Elephant struct {
	UseTest  bool
	numElves int
}

func (this *Elephant) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		n, _ := strconv.Atoi(line)
		this.numElves = n
	}
	defer file.Close()
}

func (this *Elephant) getLastElf(isPart2 bool) int {
	target := float64(this.numElves)
	if !isPart2 {
		logResult := int(math.Log2(target))
		indexOdd := int(target) - int(math.Pow(2, float64(logResult)))
		return indexOdd*2 + 1
	} else {
		logResult := int(math.Log(target) / math.Log(3))
		power3 := int(math.Pow(3, float64(logResult)))
		index := int(target) - power3
		if index == 0 {
			return power3
		} else if index <= power3 {
			return index
		}
		return power3 + (index-power3)*2
	}
}

func main() {
	elephant := &Elephant{
		UseTest: false,
	}
	elephant.getInput()
	fmt.Println("Day 19 part 1:", elephant.getLastElf(false))
	fmt.Println("Day 19 part 2:", elephant.getLastElf(true))
}
