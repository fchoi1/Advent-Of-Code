package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
)

type Rolls struct {
	useTest bool
	grid    [][]rune
	part1   int
	part2   int
}

func (this *Rolls) getInput() {
	inputFile := "input.txt"
	if this.useTest {
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

func (this *Rolls) countRolls(x, y int) int {
	H := len(this.grid)
	W := len(this.grid[0])
	count := 0
	dirs := [][2]int{
		{0, 1},
		{1, 0},
		{1, 1},
		{-1, 0},
		{0, -1},
		{-1, -1},
		{1, -1},
		{-1, 1},
	}
	for _, d := range dirs {
		nx := x + d[0]
		ny := y + d[1]
		if nx >= 0 && nx < W && ny >= 0 && ny < H {
			if this.grid[ny][nx] == '@' {
				count++
			}
		}
	}

	return count
}

func (this *Rolls) countAll() int {
	count := 0
	for y, row := range this.grid {
		for x, char := range row {
			if char == '@' {
				if this.countRolls(x, y) < 4 {
					count++
				}
			}
		}
	}
	return count
}

func (this *Rolls) remove() int {

	count := 0
	for {
		removed := false
		for y, row := range this.grid {
			for x, char := range row {
				if char == '@' {
					if this.countRolls(x, y) < 4 {
						count++
						this.grid[y][x] = '.'
						removed = true
					}
				}
			}
		}
		if !removed {
			break
		}
	}

	return count
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()

	rolls := &Rolls{
		useTest: *useTest,
	}
	rolls.getInput()
	fmt.Println("Day 2 part 1:", rolls.countAll())
	fmt.Println("Day 2 part 2:", rolls.remove())
}
