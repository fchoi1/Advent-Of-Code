package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
)

type Binary struct {
	useTest    bool
	binaryList []string
}

func (this *Binary) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.binaryList = append(this.binaryList, line)
	}
	defer file.Close()
}

func (this *Binary) getBinary(list string) int {
	var binary int
	for i, val := range list {
		if val == '1' {
			binary += int(math.Pow(2, float64(len(list)-i-1)))
		}
	}
	return binary
}

func (this *Binary) getPower() int {
	N := len(this.binaryList[0])
	counts := make([]int, N)
	var gamma int
	for _, binary := range this.binaryList {
		for i, bit := range binary {
			if bit == '1' {
				counts[i]++
			}
		}
	}
	for i, count := range counts {
		if count > len(this.binaryList)/2 {
			gamma += int(math.Pow(2, float64(N-i-1)))
		}
	}
	return gamma * (gamma ^ this.getBinary(strings.Repeat("1", N)))
}

func (this *Binary) getFiltered(index int, list []string, reverse bool) []string {
	var count int
	countList := [][]string{{}, {}}
	for _, binary := range list {
		if binary[index] == '1' {
			count++
			countList[1] = append(countList[1], binary)
		} else {
			countList[0] = append(countList[0], binary)
		}
	}
	half := (len(list) + 1) / 2
	if (count >= half && !reverse) || (count < half && reverse) {
		return countList[1]
	}
	return countList[0]

}

func (this *Binary) getLifeSupport() int {
	N := len(this.binaryList[0])
	oxygen := this.binaryList
	co2 := this.binaryList

	for i := 0; i < N; i++ {
		if len(oxygen) > 1 {
			oxygen = this.getFiltered(i, oxygen, false)
		}
		if len(co2) > 1 {
			co2 = this.getFiltered(i, co2, true)
		}
	}
	return this.getBinary(oxygen[0]) * this.getBinary(co2[0])
}

func main() {
	binary := &Binary{
		useTest: false,
	}
	binary.getInput()
	fmt.Println("Day 3 part 1:", binary.getPower())
	fmt.Println("Day 3 part 2:", binary.getLifeSupport())
}
