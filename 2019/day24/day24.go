package main

import (
	"bufio"
	"fmt"
	"os"
)

type Shuffler struct {
	UseTest bool
	grid    [][]rune
	height  int
	width   int
}

func isEmpty(grid [][]rune) bool {
	for _, row := range grid {
		for _, val := range row {
			if val == '#' {
				return false
			}
		}
	}
	return true
}

func (this *Shuffler) getInput() {
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

func (this *Shuffler) generateKey(grid [][]rune) string {
	var str string
	for _, row := range grid {
		for _, val := range row {
			str += string(val)
		}
		str += ";"
	}
	return str
}

func (this *Shuffler) countBugs(grid [][]rune, x int, y int) int {
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

func (this *Shuffler) countBugs2(grid [][]rune, innerGrid [][]rune, outerGrid [][]rune, x int, y int) int {
	var count int
	if x == 2 && y == 2 {
		return 0
	}
	for _, dir := range [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
		dx, dy := dir[0], dir[1]

		if len(innerGrid) > 0 && x+dx == 2 && y+dy == 2 {
			for i := 0; i < 5; i++ {
				if dx == 1 && innerGrid[i][0] == '#' {
					count++
				} else if dx == -1 && innerGrid[i][4] == '#' {
					count++
				} else if dy == 1 && innerGrid[0][i] == '#' {
					count++
				} else if dx == -1 && innerGrid[4][i] == '#' {
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
			// if x+dx == 2 && y+dy == 2 {
			// 	continue
			// }
			if grid[y+dy][x+dx] == '#' {
				count++
			}
		}
	}
	return count
}

func (this *Shuffler) runRound(grid, inner, outer [][]rune, isPart2 bool) [][]rune {
	temp := [][]rune{}
	if len(grid) == 0 {
		grid = make([][]rune, 5)
		for i := range grid {
			grid[i] = []rune{46, 46, 46, 46, 46}
		}
	}
	fmt.Println("grid", grid, inner, outer)

	for y, row := range grid {
		tempRow := []rune{}
		for x, bug := range row {
			if x == 2 && y == 2 {
				tempRow = append(tempRow, '.')
				continue
			}
			var bugs int
			if isPart2 {
				bugs = this.countBugs2(grid, inner, outer, x, y)
				// fmt.Println("bugs", x, y, bugs)
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

func (this *Shuffler) runLife() {
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

func (this *Shuffler) getRating() int {
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

func (this *Shuffler) getBugs() int {
	this.getInput()
	time := 10
	grids := make([][][]rune, time*2)
	var t int
	grids[time] = this.grid
	for t < time+1 {

		prevInnerGrid := this.runRound(grids[time], grids[time-1], grids[time+1], true)
		prevOuterGrid := prevInnerGrid
		fmt.Println("lvl 0", t)
		for _, row := range prevInnerGrid {
			fmt.Println(string(row))
		}

		for i := 0; i < time-1; i++ {
			// mid
			tempInner := this.runRound(grids[time-i-1], grids[time-i-2], grids[time-i], true)
			grids[time-i] = prevInnerGrid
			prevInnerGrid = tempInner

			tempOuter := this.runRound(grids[time+i+1], grids[time+i], grids[time+i+2], true)
			grids[time+i] = prevOuterGrid
			prevOuterGrid = tempOuter
			fmt.Println("loop", i)

			if isEmpty(tempInner) || isEmpty(tempOuter) {
				fmt.Println("BROKEN")
				break
			}

			// middle
			// grids[200] =
			// outward
		}
		t += 1
	}

	for x, grid := range grids {
		fmt.Println("DEPTH #", x-time)
		for _, row := range grid {
			fmt.Println(string(row))
		}
	}
	return 1
}

func main() {
	shuffler := &Shuffler{
		UseTest: true,
	}
	// fmt.Println("Day 24 part 1:", shuffler.getRating())
	fmt.Println("Day 24 part 2:", shuffler.getBugs())
}
