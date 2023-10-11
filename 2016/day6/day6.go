package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
)

type Signal struct {
	UseTest bool
	Codes   []string
	maxCode string
	minCode string
	Counter []map[string]int
}

type Counter struct {
	char  string
	count int
}

func (this *Signal) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.Codes = append(this.Codes, line)
	}
	defer file.Close()
}

func (this *Signal) countCharacters() {
	length := len(this.Codes[0])
	this.Counter = make([]map[string]int, length)
	maxCounts := make([]Counter, length)

	for i := range this.Counter {
		this.Counter[i] = make(map[string]int)
	}

	for _, code := range this.Codes {
		for i, char := range code {
			strChr := string(char)
			this.Counter[i][strChr]++

			if this.Counter[i][strChr] > maxCounts[i].count {
				maxCounts[i].count = this.Counter[i][strChr]
				maxCounts[i].char = string(strChr)
			}
		}
	}

	for i := 0; i < length; i++ {
		this.maxCode += maxCounts[i].char
		minCount := math.MaxInt64
		lowestChar := ""
		for char, count := range this.Counter[i] {
			if count < minCount {
				minCount = count
				lowestChar = char
			}
		}
		this.minCode += lowestChar
	}
}

func (this *Signal) getCode(isPart2 bool) string {
	if isPart2 {
		return this.minCode
	}
	return this.maxCode
}

func main() {
	signal := &Signal{
		UseTest: false,
	}
	signal.getInput()
	signal.countCharacters()
	fmt.Println("Day 6 part 1:", signal.getCode(false))
	fmt.Println("Day 6 part 2:", signal.getCode(true))
}
