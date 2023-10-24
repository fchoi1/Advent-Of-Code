package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
)

type HVAC struct {
	UseTest   bool
	Map       [][]rune
	Locations map[int][]int
	Width     int
	Height    int
	adjMap    map[int][]int
	steps     int
	start     int
}

func (this *HVAC) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.Map = [][]rune{}
	this.Locations = make(map[int][]int)
	j := 0
	for scanner.Scan() {
		line := scanner.Text()
		this.Map = append(this.Map, []rune(line))

		for i, char := range line {
			if hasLocation(char) {
				this.Locations[int(char-'0')] = []int{i, j}
			}
		}
		j++
	}
	this.Width = len(this.Map[0])
	this.Height = len(this.Map)
	defer file.Close()
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func hasLocation(targetRune rune) bool {
	runeList := []rune{'0', '1', '2', '3', '4', '5', '6', '7'}
	for _, r := range runeList {
		if r == targetRune {
			return true
		}
	}
	return false
}

func (this *HVAC) makeAdjacencyMap() {
	this.adjMap = make(map[int][]int)
	for start, startCoord := range this.Locations {
		runeList := make([]int, len(this.Locations))
		for end, endCoord := range this.Locations {
			if end == start {
				continue
			}
			steps := this.bfs(startCoord, endCoord)
			runeList[end] = steps
		}
		this.adjMap[start] = runeList
	}
}

func (this *HVAC) bfs(start, goal []int) int {
	steps := 0
	dirMap := [][]int{{0, -1}, {0, 1}, {1, 0}, {-1, 0}}
	queue := [][]int{start}
	visited := make(map[string]bool)
	for len(queue) > 0 {
		temp := [][]int{}
		for _, curr := range queue {
			if curr[0] == goal[0] && curr[1] == goal[1] {
				return steps
			}
			for _, dir := range dirMap {
				newX, newY := dir[0]+curr[0], dir[1]+curr[1]
				key := strconv.Itoa(newX) + "," + strconv.Itoa(newY)
				if visited[key] || this.Map[newY][newX] == '#' {
					continue
				}
				visited[key] = true
				if newX >= 0 && newX < this.Width && newY >= 0 && newY < this.Height {
					temp = append(temp, []int{newX, newY})
				}
			}
		}
		steps++
		queue = temp
	}
	return -1
}

func (this *HVAC) getShortestPath(curr int, visited map[int]bool, totalCost int, isPart2 bool) {
	if visited[curr] {
		return
	}
	visited[curr] = true
	if len(visited) == len(this.Locations) {
		if isPart2 {
			totalCost += this.adjMap[curr][0]
		}
		this.steps = min(this.steps, totalCost)
		return
	}
	for path, cost := range this.adjMap[curr] {
		if visited[path] {
			continue
		}
		this.getShortestPath(path, visited, totalCost+cost, isPart2)
		delete(visited, path)
	}
}

func (this *HVAC) getLeastSteps(isPart2 bool) int {
	this.makeAdjacencyMap()
	this.steps = math.MaxInt64
	this.start = 0
	this.getShortestPath(0, make(map[int]bool), 0, isPart2)

	return this.steps
}

func main() {
	hvac := &HVAC{
		UseTest: false,
	}
	hvac.getInput()
	fmt.Println("Day 24 part 1:", hvac.getLeastSteps(false))
	fmt.Println("Day 24 part 2:", hvac.getLeastSteps(true))
}
