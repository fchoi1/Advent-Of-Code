package main

import (
	"bufio"
	"fmt"
	"os"
)

type Dragon struct {
	UseTest bool
	Num     string
}

func (this *Dragon) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.Num = scanner.Text()
	}
	defer file.Close()
}

func reverse(s string) string {
	rns := []rune(s) // convert to rune
	for i, j := 0, len(rns)-1; i < j; i, j = i+1, j-1 {
		rns[i], rns[j] = rns[j], rns[i]
	}
	for i, char := range rns {
		if char == '0' {
			rns[i] = '1'
			continue
		}
		rns[i] = '0'
	}
	return string(rns)
}

func (this *Dragon) processChecksum(isPart2 bool) string {
	var targetLength int
	if this.UseTest {
		targetLength = 20
	} else {
		targetLength = 272
	}
	if isPart2 {
		targetLength = 35_651_584
	}
	binStr := this.Num
	for len(binStr) < targetLength {
		b := reverse(binStr)
		binStr = binStr + "0" + b
	}
	checksum := getChecksum(binStr[:targetLength])
	return checksum
}

func getChecksum(input string) string {
	if len(input) == 2 {
		if input[0] == input[1] {
			return "1"
		}
		return "0"
	}
	half := len(input) / 2
	if half%2 == 0 {
		return getChecksum(getChecksum(input[:half]) + getChecksum(input[half:]))
	} else {
		temp := ""
		for i := 0; i < len(input); i += 2 {
			if input[i] == input[i+1] {
				temp += "1"
			} else {
				temp += "0"
			}
		}
		return temp
	}
}

func main() {
	dragon := &Dragon{
		UseTest: false,
	}
	dragon.getInput()
	fmt.Println("Day 16 part 1:", dragon.processChecksum(false))
	fmt.Println("Day 16 part 2:", dragon.processChecksum(true))
	// Total Runtime ~ 1.3s
}
