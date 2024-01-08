package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Rocket struct {
	UseTest bool
	Line2   []string
	Line1   []string
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

func (this *Rocket) getInput() {
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

func (this *Rocket) getDistance(isPart2 bool) int {
	dirMap := map[string][2]int{
		"U": {0, -1},
		"D": {0, 1},
		"L": {-1, 0},
		"R": {1, 0},
	}
	seen1, seen2 := make(map[[2]int]int), make(map[[2]int]int)
	sc1, sc2 := 0, 0
	pos1, pos2 := [2]int{0, 0}, [2]int{0, 0}
	dist, minSteps := math.MaxInt64, math.MaxInt64
	length := max(len(this.Line1), len(this.Line2))

	for i := 0; i < length; i++ {
		println("steps", sc1, sc2)
		if i < len(this.Line1) {
			dir1 := string(this.Line1[i][0])
			step1, _ := strconv.Atoi(this.Line1[i][1:])
			j := 0
			for j < step1 {
				pos1[0] += dirMap[dir1][0]
				pos1[1] += dirMap[dir1][1]
				_, stepSeen := seen1[pos1]
				if !stepSeen {
					seen1[pos1] = sc1
				}
				count, exists := seen2[pos1]
				if exists {
					fmt.Println("intersect", pos1)

					if dist > abs(pos1[0])+abs(pos1[1]) {
						dist = abs(pos1[0]) + abs(pos1[1])
					}
					if minSteps > count+seen1[pos1] {
						minSteps = count + seen1[pos1]
					}

				}
				j += 1
				sc1 += 1
			}
		}
		if i < len(this.Line2) {
			dir2 := string(this.Line2[i][0])
			step2, _ := strconv.Atoi(this.Line2[i][1:])
			k := 0
			for k < step2 {
				pos2[0] += dirMap[dir2][0]
				pos2[1] += dirMap[dir2][1]
				_, stepSeen := seen2[pos2]
				if !stepSeen {
					seen2[pos2] = sc2
				}
				count, exists := seen1[pos2]
				if exists {
					fmt.Println("intersect", pos2)
					if dist > abs(pos2[0])+abs(pos2[1]) {
						dist = abs(pos2[0]) + abs(pos2[1])
					}
					if minSteps > count+seen2[pos2] {
						minSteps = count + seen2[pos1]
					}
				}
				k += 1
				sc2 += 2
			}
		}
	}
	fmt.Println(dist, minSteps,)
	if isPart2 {
		return minSteps
	}
	return dist
}

func main() {
	rocket := &Rocket{
		UseTest: true,
		Line2:   []string{},
		Line1:   []string{},
	}
	rocket.getInput()
	fmt.Println("Day 1 part 1:", rocket.getDistance(false))
	fmt.Println("Day 1 part 1:", rocket.getDistance(true))
}
