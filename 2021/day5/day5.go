package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Hydrothermal struct {
	useTest    bool
	coords     [][]point
	firstScore int
}

type point struct {
	x, y int
}

func (this *Hydrothermal) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.coords = [][]point{}
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Split(line, " -> ")

		x1, _ := strconv.Atoi(strings.Split(splitted[0], ",")[0])
		y1, _ := strconv.Atoi(strings.Split(splitted[0], ",")[1])

		x2, _ := strconv.Atoi(strings.Split(splitted[1], ",")[0])
		y2, _ := strconv.Atoi(strings.Split(splitted[1], ",")[1])
		this.coords = append(this.coords, []point{{x1, y1}, {x2, y2}})

	}
	defer file.Close()
}

func (this *Hydrothermal) countOverlap(isPart2 bool) int {
	pointMap := make(map[point]int)
	count := 0
	for _, line := range this.coords {
		p1 := line[0]
		p2 := line[1]
		if p1.x == p2.x {
			for i := min(p1.y, p2.y); i <= max(p1.y, p2.y); i++ {
				pointMap[point{p1.x, i}]++
				if pointMap[point{p1.x, i}] == 2 {
					count++
				}
			}
		} else if p1.y == p2.y {
			for i := min(p1.x, p2.x); i <= max(p1.x, p2.x); i++ {
				pointMap[point{i, p1.y}]++
				if pointMap[point{i, p1.y}] == 2 {
					count++
				}
			}
		} else if isPart2 {
			start, end := p1, p2

			if p1.x > p2.x {
				start, end = p2, p1
			}

			for start != end {
				if pointMap[start]++; pointMap[start] == 2 {
					count++
				}
				start.x++
				if end.y > start.y {
					start.y++
				} else {
					start.y--
				}
			}
			if pointMap[start]++; pointMap[start] == 2 {
				count++
			}
		}
	}
	return count
}

func main() {
	Hydrothermal := &Hydrothermal{
		useTest: false,
	}
	Hydrothermal.getInput()
	fmt.Println("Day 5 part 1:", Hydrothermal.countOverlap(false))
	fmt.Println("Day 5 part 2:", Hydrothermal.countOverlap(true))
}
