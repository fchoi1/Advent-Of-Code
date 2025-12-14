package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Christmas struct {
	useTest  bool
	part1    int
	part2    int
	presents []Present
	grids    []Grid
}

type Present struct {
	coords map[Coord]bool
	size   int
}

type Coord struct {
	x int
	y int
}

type Grid struct {
	width  int
	height int
	sizes  []int
}

func (this *Christmas) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	currCoords := []string{}

	numShapes := 0
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {

			if numShapes == 6 {
				numShapes += 1
			}
			continue
		}
		if numShapes > 6 {

			parts := strings.Split(line, ": ")
			dimensions := strings.Split(parts[0], "x")
			x, _ := strconv.Atoi(dimensions[0])
			y, _ := strconv.Atoi(dimensions[1])

			sizeStr := strings.Split(parts[1], " ")
			sizes := []int{}
			for _, size := range sizeStr {
				s, _ := strconv.Atoi(string(size))
				sizes = append(sizes, s)

			}
			this.grids = append(this.grids, Grid{x, y, sizes})

		} else {

			if line[1] == ':' {
				numShapes += 1
				present := parseCoord(currCoords)
				this.presents = append(this.presents, Present{present, len(present)})
				currCoords = []string{}

			} else {
				currCoords = append(currCoords, line)
			}
		}
	}
	defer file.Close()
}

func parseCoord(grid []string) map[Coord]bool {
	coords := make(map[Coord]bool)
	for y, row := range grid {
		for x, val := range row {
			if val == '#' {
				coords[Coord{x, y}] = true
			}
		}
	}
	return coords
}

// A bit lame solution using information heuristic (i.e approximation)
func (this *Christmas) getPart1() int {
	count := 0
	for _, g := range this.grids {
		allowable := (g.height / 3 * g.width / 3)

		total := 0
		for _, amount := range g.sizes {
			total += amount
		}

		// Approximate
		if total > allowable {
			continue
		}
		count += 1
	}
	return count
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()
	christmas := &Christmas{
		useTest: *useTest,
	}
	christmas.getInput()
	fmt.Println("Day 12 part 1:", christmas.getPart1())
}
