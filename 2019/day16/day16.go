package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type GameMap struct {
	UseTest   bool
	numstr    string
	numLength int
}

func (this *GameMap) getInput() {
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
	fmt.Println(len(this.numstr))
	defer file.Close()
}

func (this *GameMap) getFullPhaseVal(strNum string) []int {
	phaseVal := []int{}
	str := strings.Repeat(strNum, this.numLength)
	for i := 0; i < this.numLength; i++ {
		length := (4 * (i + 1))
		val := this.getPhaseVal(i, str[:length])
		phaseVal = append(phaseVal, val)
	}
	return phaseVal
}

func (this *GameMap) getPhaseVal(index int, strNum string) int {
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
func (this *GameMap) FFT(strNum string) string {
	var numStr string
	for i := 0; i < this.numLength; i++ {
		length := (4 * (i + 1))
		val := this.getPhaseVal(i, strNum)
		if val < 0 {
			val *= -1
		}
		fmt.Println("\nnum", i, "val", val, this.numLength, length)
		fmt.Println("calcs", this.numLength/length, this.numLength%length)
		fmt.Println("calc2", length/this.numLength, length%this.numLength)

		lastDigit := val % 10
		numStr += strconv.Itoa(lastDigit)
	}
	return numStr
}

func (this *GameMap) runFFT() string {
	phases := 1
	str := this.numstr
	var i int
	for i < phases {
		str = this.FFT(str)
		i += 1
	}
	// fmt.Println(str[:8], str[8:16])
	return str
}

// 1 2 3 4   5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
// + . - .   + . - . + . - . + . - . + . - . + . - . + . - . + . - . + . - . + . - .
// 4 * 5
// 1 2 3 4 5 6 7 8
// . + + . . - - .
// 8 * 5
// 1 2 3 4 5 6 7 8 1 2 3 4
// . . + + + . . . - - - .
// 12 - 6 = 6 * 3 + 7 = 18 + 7 = 25
// 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
// . . . + + + + . . . . - - - - .

// 4 + 5 + 6 + 7

// 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
// . . . . . . . + + + + + + + . . . . . . . - - - - - - - . . . . . . . + + + + +
// 1 2 3 4 5 6 7 8 (1 2 3 4 5 6 7 8) 1 2 3 4 5 6 7 8 1 2 3 (4 5 6 7 8 1 2 3) 4 5 6 7 8
// . . . . . . . .  + + + + + + + +  + . . . . . . . . . -  - - - - - - - - . . . . .
// 1 2 3 4 5 6 7 8 1 (2 3 4 5 6 7 8 1) 2 3 4 5 6 7 8 1 2 3 4 5 6 7 (8 1 2 3 4 5 6 7 8)
// . . . . . . . . .  + + + + + + + +  + + . . . . . . . . . . - -  - - - - - - - - .
// 1 2 3 4 5 6 7 8 1 2 (3 4 5 6 7 8 1 2) 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
// . . . . . . . . . .  + + + + + + + +  + + + . . . . . . . . . . . - - - - - - - -
// 1 2 3 4 5 6 7 8 1 2 3 (4 5 6 7 8) 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 ||1 2 3 4 5 6 7
// . . . . . . . . . . .  + + + + +  + + + + + + + . . . . . . . . . . . . - - - - - ||- - - - - - -
// 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 ||1 2 3 4 5 6 7
// . . . . . . . . . . . . + + + + + + + + + + + + + . . . . . . . . . . . . . - - ||- - - - - - - - - - -
// 11 cut off, last 11

// 8 % 12 = 4 -> 12 + 4
func (this *GameMap) FFT2(strNum string) string {
	this.numstr = "12345678"
	this.numLength = len(this.numstr)
	var numStr string
	var val, remainVal int
	fullPhase := this.getFullPhaseVal(strNum)
	newLength := this.numLength * 5
	str := strings.Repeat(strNum, this.numLength)

	for i := 0; i < newLength; i++ {
		// if i%1000 == 0 {
		// 	fmt.Println(i, newLength)
		// }
		length := (4 * (i + 1))
		phaseVal := fullPhase[i%this.numLength]

		times := newLength / length
		remain := newLength % length
		if remain != 0 {
			remainVal = this.getPhaseVal(i, str[:remain])
		}
		val = phaseVal*times + remainVal
		if val < 0 {
			val *= -1
		}
		// fmt.Println("\nnum", i, "val", val, remainVal, newLength, length, remain, length-remain, str[:remain])
		// fmt.Println("calcs", this.numLength/length, this.numLength%length)
		// fmt.Println("calc2", length/this.numLength, length%this.numLength)

		lastDigit := val % 10
		numStr += strconv.Itoa(lastDigit)
	}
	return numStr
}

func (this *GameMap) runFFT2() string {
	repeatedStr := strings.Repeat(this.numstr, 5)
	var i int
	for i < 1 {
		repeatedStr = this.FFT2(repeatedStr)
		i += 1
	}

	return repeatedStr
}
func main() {
	gameMap := &GameMap{
		UseTest: true,
	}
	gameMap.getInput()
	fmt.Println("Day 16 part 1:", gameMap.runFFT())
	fmt.Println("Day 16 part 2:", gameMap.runFFT2())
}

//00524718
