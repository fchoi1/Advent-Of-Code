package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"unicode"
)

type Node struct {
	name  rune
	keys  string
	doors string
	steps int
}

type Coord struct {
	name  rune
	steps int
}

type Robot struct {
	UseTest   bool
	grid      [][]rune
	adjGrid   map[rune][]Coord
	start     []int
	starts    [][]int
	totalKeys int
}

func runeInString(str string, target rune) bool {
	for _, r := range str {
		if r == target {
			return true
		}
	}
	return false
}

func sortString(s string) string {
	chars := []rune(s)
	sort.Slice(chars, func(i, j int) bool {
		return chars[i] < chars[j]
	})
	sortedString := string(chars)
	return sortedString
}

func (this *Robot) getInput() {
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
	for y, row := range this.grid {
		for x, char := range row {
			if char == '@' {
				this.start = []int{x, y}
			}
		}
	}
	defer file.Close()
}

func (this *Robot) generateList() {
	this.adjGrid = make(map[rune][]Coord)
	for y, row := range this.grid {
		for x, char := range row {
			if char != '.' && char != '#' {
				if !unicode.IsUpper(char) {
					this.totalKeys++
				}
				this.generate(char, []int{x, y})
			}
		}
	}
}

func (this *Robot) inRange(x int, y int) bool {
	inBounds := x >= 0 && x < len(this.grid[0]) && y >= 0 && y < len(this.grid)
	if !inBounds {
		return false
	}
	return this.grid[y][x] != '#'
}

// shortest paths,
func (this *Robot) generate(startName rune, start []int) {
	this.adjGrid[startName] = []Coord{}
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
			char := this.grid[y][x]

			if char != '.' && char != '#' && char != startName {
				this.adjGrid[startName] = append(this.adjGrid[startName], Coord{char, steps})
				continue
			}

			seen[key] = true
			for _, inc := range [][]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
				if this.inRange(x+inc[0], y+inc[1]) && this.grid[y+inc[1]][x+inc[0]] != '#' {
					temp = append(temp, []int{x + inc[0], y + inc[1]})
				}
			}
		}
		q = temp
		steps++
	}
}

func (this *Robot) bfs(starts []rune) int {

	q := []Node{}

	for _, r := range starts {
		q = append(q, Node{r, string(r), "", 0})
	}
	seen := make(map[string]int)
	minSteps := math.MaxInt32
	for len(q) > 0 {
		temp := []Node{}
		for _, node := range q {
			strKey := string(node.name) + ":" + node.keys + ":" + node.doors
			if val, ok := seen[strKey]; ok {
				if node.steps >= val {
					continue
				}
			}
			seen[strKey] = node.steps
			if len(node.keys) == this.totalKeys {
				if node.steps < minSteps {
					minSteps = node.steps
				}
			}

			for _, coord := range this.adjGrid[node.name] {

				if node.name == coord.name || unicode.IsUpper(coord.name) && !runeInString(node.keys, unicode.ToLower(coord.name)) {
					continue
				}

				newKeys := node.keys
				newDoors := node.doors

				if !unicode.IsUpper(coord.name) && !runeInString(node.keys, coord.name) {
					newKeys += string(coord.name)
				} else if unicode.IsUpper(coord.name) && !runeInString(node.doors, coord.name) {
					newDoors += string(coord.name)
				}
				temp = append(temp, Node{coord.name, sortString(newKeys), sortString(newDoors), node.steps + coord.steps})
			}
		}
		if minSteps < math.MaxInt32 {
			return minSteps
		}
		q = temp
	}
	return -1
}

func (this *Robot) getSteps() int {
	this.getInput()
	this.generateList()
	return this.bfs([]rune{'@'})
}
func (this *Robot) getSteps2() int {
	this.getInput()
	this.grid[this.start[1]][this.start[0]] = '#'
	this.grid[this.start[1]-1][this.start[0]] = '#'
	this.grid[this.start[1]+1][this.start[0]] = '#'
	this.grid[this.start[1]][this.start[0]-1] = '#'
	this.grid[this.start[1]][this.start[0]+1] = '#'
	this.grid[this.start[1]+1][this.start[0]+1] = '1'
	this.grid[this.start[1]-1][this.start[0]+1] = '2'
	this.grid[this.start[1]-1][this.start[0]-1] = '3'
	this.grid[this.start[1]+1][this.start[0]-1] = '4'
	this.generateList()
	for key, val := range this.adjGrid {
		fmt.Println()
		fmt.Print(string(key), " ==> ")
		for _, coord := range val {
			fmt.Print("  ", string(coord.name), ":", coord.steps)
		}
	}
	return this.bfs([]rune{'1', '2', '3', '4'})
}

func main() {
	robot := &Robot{
		UseTest: false,
	}
	// fmt.Println("Day 18 part 1:", robot.getSteps())
	fmt.Println("Day 18 part 2:", robot.getSteps2())
}
