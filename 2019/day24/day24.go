package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type LifeGame struct {
	UseTest bool
	grid    [][]rune
	height  int
	width   int
}

func (this *LifeGame) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.grid = [][]rune{}

	for scanner.Scan() {
		line := scanner.Text()
		this.grid = append(this.grid, []rune(line))
	}
	this.width = 5
	this.height = 5
	defer file.Close()
}

func (this *LifeGame) generateKey(grid [][]rune) string {
	var str string
	for _, row := range grid {
		for _, val := range row {
			str += string(val)
		}
		str += ";"
	}
	return str
}

func (this *LifeGame) countBugs(grid [][]rune, x int, y int) int {
	var count int
	for _, dir := range [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
		dx, dy := dir[0], dir[1]
		if x+dx >= 0 && x+dx < this.width && y+dy >= 0 && y+dy < this.height {
			if grid[y+dy][x+dx] == '#' {
				count++
			}
		}
	}
	return count
}

func (this *LifeGame) countBugs2(grid [][]rune, innerGrid [][]rune, outerGrid [][]rune, x int, y int) int {
	var count int
	if x == 2 && y == 2 {
		return 0
	}
	for _, dir := range [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
		dx, dy := dir[0], dir[1]

		if len(innerGrid) > 0 && x+dx == 2 && y+dy == 2 {
			for i := 0; i < 5; i++ {
				if dx == -1 && innerGrid[i][4] == '#' {
					count++
				} else if dx == 1 && innerGrid[i][0] == '#' {
					count++
				} else if dy == -1 && innerGrid[4][i] == '#' {
					count++
				} else if dy == 1 && innerGrid[0][i] == '#' {
					count++
				}
			}
		}

		if len(outerGrid) > 0 {
			if x+dx < 0 {
				if outerGrid[2][1] == '#' {
					count++
				}
			} else if x+dx >= this.width {
				if outerGrid[2][3] == '#' {
					count++
				}
			} else if y+dy < 0 {
				if outerGrid[1][2] == '#' {
					count++
				}
			} else if y+dy >= this.height {
				if outerGrid[3][2] == '#' {
					count++
				}
			}
		}
		if x+dx >= 0 && x+dx < this.width && y+dy >= 0 && y+dy < this.height {
			if grid[y+dy][x+dx] == '#' {
				count++
			}
		}
	}
	return count
}

func (this *LifeGame) runRound(grid, inner, outer [][]rune, isPart2 bool) [][]rune {
	temp := [][]rune{}
	if len(grid) == 0 {
		grid = make([][]rune, 5)
		for i := range grid {
			grid[i] = []rune{46, 46, 46, 46, 46}
		}
	}

	for y, row := range grid {
		tempRow := []rune{}
		for x, bug := range row {
			var bugs int
			if isPart2 {
				if x == 2 && y == 2 {
					tempRow = append(tempRow, '.')
					continue
				}
				bugs = this.countBugs2(grid, inner, outer, x, y)
			} else {
				bugs = this.countBugs(grid, x, y)
			}
			newBug := '.'
			if (bug == '.' && (bugs == 1 || bugs == 2)) || (bug == '#' && bugs == 1) {
				newBug = '#'
			}
			tempRow = append(tempRow, newBug)
		}
		temp = append(temp, tempRow)
	}
	return temp
}

func (this *LifeGame) runLife() {
	seen := make(map[string]bool)
	key := this.generateKey(this.grid)
	seen[key] = true
	for {
		this.grid = this.runRound(this.grid, [][]rune{}, [][]rune{}, false)
		key := this.generateKey(this.grid)
		if _, ok := seen[key]; ok {
			break
		}
		seen[key] = true
	}
}

func (this *LifeGame) getRating() int {
	this.getInput()
	this.runLife()
	val := 1
	var rating int
	for _, row := range this.grid {
		for _, bug := range row {
			if bug == '#' {
				rating += val
			}
			val *= 2
		}
	}
	return rating
}

func (this *LifeGame) getBugs() int {
	this.getInput()
	time := 200
	if this.UseTest {
		time = 10
	}
	grids := make([][][]rune, (time+1)*2)
	var t int
	grids[time] = this.grid
	for t < time {
		tempGrid := make([][][]rune, (time+1)*2)
		var prevGrid [][]rune
		for i, grid := range grids {
			if i == 0 || i == len(tempGrid)-1 {
				prevGrid = grid
				continue
			}
			tempGrid[i] = this.runRound(grid, grids[i+1], prevGrid, true)
			prevGrid = grid
		}
		grids = tempGrid
		t += 1
	}
	var totalBugs int
	for _, grid := range grids {
		for _, row := range grid {
			totalBugs += strings.Count(string(row), "#")
		}
	}
	return totalBugs
}

func main() {
	lifeGame := &LifeGame{
		UseTest: false,
	}
	fmt.Println("Day 24 part 1:", lifeGame.getRating())
	fmt.Println("Day 24 part 2:", lifeGame.getBugs())
}
