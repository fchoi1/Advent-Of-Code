package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Capsule struct {
	UseTest bool
	Discs   [][]int
}

func (this *Capsule) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.Discs = [][]int{}
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == ' ' || r == '.'
		})
		numPos, _ := strconv.Atoi(splitted[3])
		startPos, _ := strconv.Atoi(splitted[11])
		this.Discs = append(this.Discs, []int{numPos, startPos})
	}
	defer file.Close()
}

func (this *Capsule) getTime(isPart2 bool) int {
	if isPart2 {
		this.Discs = append(this.Discs, []int{11, 0})
	}
	maxTime := math.MaxInt64
	var aligned bool

	for time := 0; time < maxTime; time++ {
		target := (time + this.Discs[0][1]) % this.Discs[0][0]
		aligned = true
		for i, disc := range this.Discs[1:] {
			i++
			pos := (disc[0] + time + i + disc[1]) % disc[0]
			if pos != target {
				aligned = false
				break
			}
		}
		if aligned {
			return time - 1
		}
	}
	return -1
}

func main() {
	capsule := &Capsule{
		UseTest: false,
	}
	capsule.getInput()
	fmt.Println("Day 15 part 1:", capsule.getTime(false))
	fmt.Println("Day 15 part 2:", capsule.getTime(true))
}
