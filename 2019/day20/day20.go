package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Donut struct {
	UseTest  bool
	grid     [][]string
	w        int
	h        int
	portals  map[string][]int
	innerMap map[string][]int
	outerMap map[string][]int
	innerDim []int
}

func (this *Donut) getInput() {
	inputFile := "input.txt"

	this.innerDim = []int{34, 92, 34, 92} // xMin, xMax, yMin, yMax
	if this.UseTest {
		inputFile = "input-test.txt"
		// Hardcoded tests
		// this.innerDim = []int{8, 26, 8, 28}
		// this.innerDim = []int{6, 14, 6, 12}
		this.innerDim = []int{8, 36, 8, 28}

	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.grid = [][]string{}

	for scanner.Scan() {
		line := scanner.Text()
		var splitted []string
		for _, char := range line {
			splitted = append(splitted, string(char))
		}
		this.grid = append(this.grid, splitted)
	}
	this.w = len(this.grid[0])
	this.h = len(this.grid)
	this.getPortals()
	defer file.Close()
}

func (this *Donut) getPortals() {
	this.outerMap = make(map[string][]int)
	this.innerMap = make(map[string][]int)
	this.portals = make(map[string][]int)

	for i := range this.grid {
		// outer left
		if this.grid[i][2] == "." {
			this.portals[this.grid[i][0]+this.grid[i][1]] = []int{2, i}
		}
		// outer right
		if this.grid[i][this.w-3] == "." {
			this.portals[this.grid[i][this.w-2]+this.grid[i][this.w-1]] = []int{this.w - 3, i}
		}
	}

	for i := range this.grid[0] {
		// outer top
		if this.grid[2][i] == "." {
			this.portals[this.grid[0][i]+this.grid[1][i]] = []int{i, 2}
		}
		// outer bot
		if this.grid[this.h-3][i] == "." {
			this.portals[this.grid[this.h-2][i]+this.grid[this.h-1][i]] = []int{i, this.h - 3}
		}
	}

	for i := this.innerDim[2]; i < this.innerDim[3]; i++ {
		// inner left
		if this.grid[i][this.innerDim[0]] == "." {
			portal := this.grid[i][this.innerDim[0]+1] + this.grid[i][this.innerDim[0]+2]
			if coord, ok := this.portals[portal]; ok {
				this.innerMap[strconv.Itoa(this.innerDim[0])+","+strconv.Itoa(i)] = coord
				this.outerMap[strconv.Itoa(coord[0])+","+strconv.Itoa(coord[1])] = []int{this.innerDim[0], i}
			}
		}
		// inner right
		if this.grid[i][this.innerDim[1]] == "." {
			portal := this.grid[i][this.innerDim[1]-2] + this.grid[i][this.innerDim[1]-1]
			if coord, ok := this.portals[portal]; ok {
				this.innerMap[strconv.Itoa(this.innerDim[1])+","+strconv.Itoa(i)] = coord
				this.outerMap[strconv.Itoa(coord[0])+","+strconv.Itoa(coord[1])] = []int{this.innerDim[1], i}
			}
		}
	}

	for i := this.innerDim[0]; i < this.innerDim[1]; i++ {
		// inner top
		if this.grid[this.innerDim[2]][i] == "." {
			portal := this.grid[this.innerDim[2]+1][i] + this.grid[this.innerDim[2]+2][i]
			if coord, ok := this.portals[portal]; ok {
				this.innerMap[strconv.Itoa(i)+","+strconv.Itoa(this.innerDim[2])] = coord
				this.outerMap[strconv.Itoa(coord[0])+","+strconv.Itoa(coord[1])] = []int{i, this.innerDim[2]}
			}
		}
		// inner bot
		if this.grid[this.innerDim[3]][i] == "." {
			portal := this.grid[this.innerDim[3]-2][i] + this.grid[this.innerDim[3]-1][i]
			if coord, ok := this.portals[portal]; ok {
				this.innerMap[strconv.Itoa(i)+","+strconv.Itoa(this.innerDim[3])] = coord
				this.outerMap[strconv.Itoa(coord[0])+","+strconv.Itoa(coord[1])] = []int{i, this.innerDim[3]}
			}
		}
	}
}
func (this *Donut) bfs(start []int, end []int) int {

	q := [][]int{start}
	seen := make(map[string]bool)
	var steps int
	for len(q) > 0 {
		temp := [][]int{}
		for _, curr := range q {
			key := strconv.Itoa(curr[0]) + "," + strconv.Itoa(curr[1])
			x, y := curr[0], curr[1]
			if x == end[0] && y == end[1] {
				return steps
			}
			if _, ok := seen[key]; ok {
				continue
			}
			seen[key] = true
			if val, ok := this.innerMap[key]; ok {
				temp = append(temp, val)
			}
			if val, ok := this.outerMap[key]; ok {
				temp = append(temp, val)
			}

			for _, dir := range [][]int{{0, 1}, {1, 0}, {-1, 0}, {0, -1}} {
				newX, newY := x+dir[0], y+dir[1]
				if this.grid[newY][newX] == "." {
					temp = append(temp, []int{newX, newY})
				}
			}
		}
		q = temp
		steps++
	}
	return -1
}

func (this *Donut) bfs2(start []int, end []int) int {

	q := [][]int{{0, start[0], start[1]}}
	seen := make(map[string]bool)
	var steps int

	for len(q) > 0 {
		temp := [][]int{}
		for _, curr := range q {
			key := strconv.Itoa(curr[0]) + "," + strconv.Itoa(curr[1]) + "," + strconv.Itoa(curr[2])
			portalKey := strconv.Itoa(curr[1]) + "," + strconv.Itoa(curr[2])
			lvl, x, y := curr[0], curr[1], curr[2]

			if _, ok := seen[key]; ok {
				continue
			}
			seen[key] = true

			if x == end[0] && y == end[1] && lvl == 0 {
				return steps
			}

			if val, ok := this.innerMap[portalKey]; ok {
				temp = append(temp, []int{lvl + 1, val[0], val[1]})
			}

			if lvl != 0 {
				if val, ok := this.outerMap[portalKey]; ok {
					temp = append(temp, []int{lvl - 1, val[0], val[1]})
				}
			}

			for _, dir := range [][]int{{0, 1}, {1, 0}, {-1, 0}, {0, -1}} {
				newX, newY := x+dir[0], y+dir[1]
				if this.grid[newY][newX] == "." {
					temp = append(temp, []int{lvl, newX, newY})
				}
			}
		}
		q = temp
		steps++
	}
	return -1
}

func (this *Donut) getSteps() int {
	return this.bfs(this.portals["AA"], this.portals["ZZ"])
}

func (this *Donut) getSteps2() int {
	return this.bfs2(this.portals["AA"], this.portals["ZZ"])
}

func main() {
	donut := &Donut{
		UseTest: false,
	}
	donut.getInput()
	fmt.Println("Day 20 part 1:", donut.getSteps())
	fmt.Println("Day 20 part 2:", donut.getSteps2())

}
