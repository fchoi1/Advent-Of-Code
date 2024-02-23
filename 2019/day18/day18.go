package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"unicode"
)

type Scaffolding struct {
	UseTest bool
	grid    [][]rune
	keys    map[rune][]int
	doors   map[rune][]int
	start   []int
}

func (this *Scaffolding) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.grid = append(this.grid, []rune(line))
	}
	defer file.Close()
}

func (this *Scaffolding) getLetters() {
	this.keys = make(map[rune][]int)
	this.doors = make(map[rune][]int)
	for y, row := range this.grid {
		for x, char := range row {
			if char != '.' && char != '#' {
				if char == '@' {
					this.start = []int{x, y}
					continue
				}
				if unicode.IsUpper(char) {
					this.doors[char] = []int{x, y}
				} else {
					this.keys[char] = []int{x, y}
				}
			}
		}
	}
}

// compress grid?
// adj list?

func (this *Scaffolding) inRange(x int, y int) bool {
	width := len(this.grid[0])
	height := len(this.grid)

	inBounds := x >= 0 && x < width && y >= 0 && y < height
	if !inBounds {
		return false
	}
	return this.grid[y][x] != '#'
}

func (this *Scaffolding) getNext(x int, y int, prevX int, prevY int) [][]int {
	nextPath := [][]int{}
	for _, inc := range [][]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
		newX := x + inc[0]
		newY := y + inc[1]
		if this.inRange(newX, newY) {
			if this.grid[newY][newX] != '#' && (newX != prevX && newY != prevY) {
				nextPath = append(nextPath, []int{x + inc[0], y + inc[1]})
			}
		}
	}
	return nextPath
}

// shortest paths,
func (this *Scaffolding) bfs(start []int, target []int) int {
	var steps, x, y int
	var key string
	q := [][]int{start}
	seen := make(map[string]bool)
	for len(q) > 0 {
		temp := [][]int{}
		for _, pos := range q {
			x, y = pos[0], pos[1]
			key = strconv.Itoa(x) + "," + strconv.Itoa(y)
			if seen[key] {
				continue
			}
			seen[key] = true
			for _, inc := range [][]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
				if this.inRange(x+inc[0], y+inc[1]) {
					temp = append(temp, []int{x + inc[0], y + inc[1]})
				}
			}

		}
		q = temp
		steps += 1
	}
	return 1
}

func (this *Scaffolding) getSteps() int {
	this.getLetters()
	fmt.Println(this.start)
	return 1
}
func (this *Scaffolding) getDust() int {
	return 1
}

func main() {
	scaffolding := &Scaffolding{
		UseTest: false,
	}
	scaffolding.getInput()
	fmt.Println("Day 18 part 1:", scaffolding.getSteps())
	// fmt.Println("Day 18 part 2:", scaffolding.getDust())
}
