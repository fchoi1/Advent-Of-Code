package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type FFT struct {
	UseTest   bool
	numstr    string
	numLength int
}

func (this *FFT) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.numstr = scanner.Text()
	}
	this.numLength = len(this.numstr)
	defer file.Close()
}

func (this *FFT) getPhaseVal(index int, strNum string) int {
	add := index
	sub := 2 + index*3
	length := (4 * (index + 1))
	var addCount, subCount, val int
	for i, char := range strNum {
		num, _ := strconv.Atoi(string(char))
		if (i-add)%length == 0 {
			addCount = index + 1
		}
		if (i-sub)%length == 0 {
			subCount = index + 1
		}
		if addCount != 0 {
			val += num
			addCount -= 1
		}
		if subCount != 0 {
			val -= num
			subCount -= 1
		}
	}
	return val
}
func (this *FFT) FFT(strNum string) string {
	var numStr string
	for i := 0; i < this.numLength; i++ {
		val := this.getPhaseVal(i, strNum)
		if val < 0 {
			val *= -1
		}
		lastDigit := val % 10
		numStr += strconv.Itoa(lastDigit)
	}
	return numStr[:8]
}

func (this *FFT) run() string {
	str := this.numstr
	for i := 0; i < 100; i++ {
		str = this.FFT(str)
	}
	return str
}

func (this *FFT) FFT2(intList []int) []int {
	var newList []int
	var sumVal int
	for _, val := range intList {
		sumVal += val
	}
	for _, val := range intList {
		newList = append(newList, sumVal%10)
		sumVal -= val
	}
	return newList
}
func (this *FFT) runHack() string {
	var intList []int
	var strList []string
	offset, _ := strconv.Atoi(this.numstr[:7])
	newStr := strings.Repeat(this.numstr, 10_000)[offset:]

	for _, char := range newStr {
		num, _ := strconv.Atoi(string(char))
		intList = append(intList, num)
	}

	for i := 0; i < 100; i++ {
		// Trick* Second half of output correspons with sum of second half of input
		// The offset only occurs on the second half
		intList = this.FFT2(intList)
	}
	for _, num := range intList[:8] {
		strList = append(strList, strconv.Itoa(num))
	}

	return strings.Join(strList, "")
}

func main() {
	FFT := &FFT{
		UseTest: false,
	}
	FFT.getInput()
	fmt.Println("Day 16 part 1:", FFT.run())
	fmt.Println("Day 16 part 2:", FFT.runHack())
}
