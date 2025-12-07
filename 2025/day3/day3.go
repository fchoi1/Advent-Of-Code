package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

type Batteries struct {
	useTest   bool
	batteries []string
	part1     int
	part2     int
}

func mod(a, b int) int {
	return (a%b + b) % b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func (this *Batteries) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.batteries = append(this.batteries, line)
	}
	defer file.Close()
}

func getJoltage(val string, digits int) int {
	// depending on digits we scan left for max allowable
	jolt := ""
	prevIdx := 0
	for i := 0; i < digits; i++ {

		maxVal := '0'
		maxIdx := -1
		// find allowable range based on prev
		for j := prevIdx; j < len(val)-(digits-i-1); j++ {
			if rune(val[j]) > maxVal {
				maxVal = rune(val[j])
				maxIdx = j
			}
		}
		jolt += string(maxVal)
		prevIdx = maxIdx + 1
	}

	converted, _ := strconv.Atoi(jolt)
	return converted
}

func (this *Batteries) getPart1() int {
	ans := 0
	for _, val := range this.batteries {
		ans += getJoltage(val, 2)
	}

	return ans
}

func (this *Batteries) getPart2() int {
	ans := 0
	for _, val := range this.batteries {
		ans += getJoltage(val, 12)
	}
	return ans
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()

	batteries := &Batteries{
		useTest: *useTest,
	}
	batteries.getInput()
	fmt.Println("Day 3 part 1:", batteries.getPart1())
	fmt.Println("Day 3 part 2:", batteries.getPart2())
}
