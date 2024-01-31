package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Office struct {
	UseTest      bool
	OfficeNum    int
	Dest         []int
	MaxLocations int
	Steps        int
}

func (this *Office) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
		this.Dest = []int{7, 4}
	} else {
		this.Dest = []int{31, 39}
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.OfficeNum, _ = strconv.Atoi(line)
	}
	defer file.Close()
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func (this *Office) findLocation(startPos []int) {
	// BFS
	dirMap := [][]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}

	visited := make(map[string]bool)
	var queue [][]int
	queue = append(queue, startPos)

	steps := 0

	for len(queue) > 0 {
		if steps == 50 {
			this.MaxLocations = len(visited)
		}
		temp := [][]int{}

		for _, currPos := range queue {
			x, y := currPos[0], currPos[1]
			if x == this.Dest[0] && y == this.Dest[1] {
				this.Steps = steps
				return
			}

			for _, dir := range dirMap {
				newX, newY := dir[0]+x, dir[1]+y
				isAWall := isWall(newX, newY, this.OfficeNum)
				key := strconv.Itoa(newX) + "," + strconv.Itoa(newY)
				_, exists := visited[key]

				if exists {
					continue
				}
				if !isAWall {
					visited[key] = true
					temp = append(temp, []int{newX, newY})
				}
			}
		}
		queue = temp
		steps++
	}
	return
}

func isWall(x int, y int, officeNum int) bool {
	if x < 0 || y < 0 {
		return true
	}
	val := x*x + 3*x + 2*x*y + y + y*y + officeNum
	count := 0
	for val != 0 {
		count += val & 1
		val >>= 1
	}
	return count%2 == 1
}

func (this *Office) getSteps() int {
	return this.Steps
}

func (this *Office) getMaxLocations() int {
	return this.MaxLocations
}

func main() {
	office := &Office{
		UseTest: false,
	}
	office.getInput()
	office.findLocation([]int{1, 1})
	fmt.Println("Day 13 part 1:", office.getSteps())
	fmt.Println("Day 13 part 2:", office.getMaxLocations())
}
