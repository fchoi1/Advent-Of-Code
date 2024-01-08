package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Wire struct {
	UseTest  bool
	Line2    []string
	Line1    []string
	minSteps int
	dist     int
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func (this *Wire) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if len(this.Line1) == 0 {
			this.Line1 = strings.Split(line, ",")
		} else {
			this.Line2 = strings.Split(line, ",")
		}
	}
	defer file.Close()
}

func (this *Wire) travel() {
	dirMap := map[string][2]int{
		"U": {0, 1},
		"D": {0, -1},
		"L": {-1, 0},
		"R": {1, 0},
	}
	seen1, seen2 := make(map[[2]int]int), make(map[[2]int]int)
	sc1, sc2 := 0, 0
	pos1, pos2 := [2]int{0, 0}, [2]int{0, 0}
	length := max(len(this.Line1), len(this.Line2))

	for i := 0; i < length; i++ {
		if i < len(this.Line1) {
			dir := string(this.Line1[i][0])
			steps, _ := strconv.Atoi(this.Line1[i][1:])
			for j := 0; j < steps; j++ {
				sc1++
				pos1[0], pos1[1] = pos1[0]+dirMap[dir][0], pos1[1]+dirMap[dir][1]
				if _, stepSeen := seen1[pos1]; !stepSeen {
					seen1[pos1] = sc1
				}
				if count, exists := seen2[pos1]; exists {
					dist := abs(pos1[0]) + abs(pos1[1])
					if this.dist > dist {
						this.dist = dist
					}
					minStep := count + seen1[pos1]
					if this.minSteps > minStep {
						this.minSteps = minStep
					}
				}
			}
		}
		if i < len(this.Line2) {
			dir := string(this.Line2[i][0])
			steps, _ := strconv.Atoi(this.Line2[i][1:])
			for j := 0; j < steps; j++ {
				sc2++
				pos2[0], pos2[1] = pos2[0]+dirMap[dir][0], pos2[1]+dirMap[dir][1]
				if _, stepSeen := seen2[pos2]; !stepSeen {
					seen2[pos2] = sc2
				}
				if count, exists := seen1[pos2]; exists {
					dist := abs(pos2[0]) + abs(pos2[1])
					if this.dist > dist {
						this.dist = dist
					}
					minStep := count + seen2[pos2]
					if this.minSteps > minStep {
						this.minSteps = minStep
					}
				}
			}
		}
	}
}

func (this *Wire) getDistance() int {
	return this.dist
}
func (this *Wire) getMinSteps() int {
	return this.minSteps
}

func main() {
	wire := &Wire{
		UseTest:  false,
		minSteps: math.MaxInt64,
		dist:     math.MaxInt64,
		Line2:    []string{},
		Line1:    []string{},
	}
	wire.getInput()
	wire.travel()
	fmt.Println("Day 1 part 1:", wire.getDistance())
	fmt.Println("Day 1 part 2:", wire.getMinSteps())
}
