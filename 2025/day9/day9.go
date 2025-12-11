package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Movie struct {
	useTest bool
	tiles   []Coord
	part1   int
	part2   int
	grid    [][]bool
	xLookup map[int]int
	yLookup map[int]int
}

type Coord struct {
	x int
	y int
}

type BorderCord struct {
	x float32
	y float32
}

func max(x, y int) int {
	if x > y {
		return x
	}
	return y
}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func (this *Movie) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		nums := strings.Split(line, ",")
		x, _ := strconv.Atoi(nums[0])
		y, _ := strconv.Atoi(nums[1])
		this.tiles = append(this.tiles, Coord{x, y})
	}
	defer file.Close()
}

// extract all x, y, form a grid
func (this *Movie) parseGrid() {
	xArr, yArr := map[int]bool{}, map[int]bool{}
	this.xLookup, this.yLookup = map[int]int{}, map[int]int{}
	for _, coord := range this.tiles {
		xArr[coord.x] = true
		yArr[coord.y] = true
	}
	xs, ys := []int{}, []int{}
	for x := range xArr {
		xs = append(xs, x)
	}
	for y := range yArr {
		ys = append(ys, y)
	}

	sort.Ints(xs)
	sort.Ints(ys)
	for i, x := range xs {
		this.xLookup[x] = i
	}
	for i, y := range ys {
		this.yLookup[y] = i
	}
	this.grid = make([][]bool, len(ys))
	for i := range this.grid {
		this.grid[i] = make([]bool, len(xs))
	}
}

func (this *Movie) getBorder() map[BorderCord]bool {
	borders := make(map[BorderCord]bool)
	N := len(this.tiles)
	var prev Coord
	for i, coord := range this.tiles {
		if i == 0 {
			prev = this.tiles[N-1]
		} else {
			prev = this.tiles[i-1]
		}
		c := this.getGridCoord(coord)
		p := this.getGridCoord(prev)
		if c.x == p.x {
			for y := min(c.y, p.y); y < max(c.y, p.y); y++ {
				borders[BorderCord{float32(c.x), float32(y) + 0.5}] = true
			}

		} else {
			for x := min(c.x, p.x); x < max(c.x, p.x); x++ {
				borders[BorderCord{float32(x) + 0.5, float32(c.y)}] = true
			}
		}
	}
	return borders
}

func (this *Movie) bfs(borders map[BorderCord]bool) {
	start := this.getGridCoord(this.tiles[0])
	if !this.useTest {
		start = Coord{start.x - 1, start.y - 1}
	}
	q := []Coord{start}
	visited := make(map[Coord]bool)

	for len(q) > 0 {
		temp := []Coord{}
		for _, coord := range q {
			if visited[coord] {
				continue
			}
			visited[coord] = true

			this.grid[coord.y][coord.x] = true
			for _, dir := range []Coord{{0, 1}, {1, 0}, {0, -1}, {-1, 0}} {
				newCoord := Coord{coord.x + dir.x, coord.y + dir.y}
				if newCoord.x < 0 || newCoord.x >= len(this.grid[0]) || newCoord.y < 0 || newCoord.y >= len(this.grid) {
					continue
				}

				var midX, midY float32

				if dir.x == 0 {
					if dir.y > 0 {
						midY = float32(newCoord.y)
					} else {
						midY = float32(coord.y)
					}
					midX = float32(coord.x) + 0.5
				} else {
					if dir.x > 0 {
						midX = float32(newCoord.x)
					} else {
						midX = float32(coord.x)
					}
					midY = float32(coord.y) + 0.5
				}

				if borders[BorderCord{midX, midY}] {
					continue
				}

				temp = append(temp, newCoord)

			}
		}
		q = temp
	}
}

func (this *Movie) isValid(c1, c2 Coord) bool {
	var x1, x2, y1, y2 int

	if c1.x == c2.x {
		return true
	} else {
		x1 = min(c1.x, c2.x)
		x2 = max(c1.x, c2.x) - 1
	}

	if c1.y == c2.y {
		return true
	} else {
		y1 = min(c1.y, c2.y)
		y2 = max(c1.y, c2.y) - 1
	}

	if this.grid[y1][x1] && this.grid[y1][x2] && this.grid[y2][x1] && this.grid[y2][x2] {
		for x := x1; x <= x2; x++ {
			if !this.grid[y1][x] || !this.grid[y2][x] {
				return false
			}
		}
		for y := y1; y <= y2; y++ {
			if !this.grid[y][x1] || !this.grid[y][x2] {
				return false
			}
		}
		return true
	}

	return false
}

func (this *Movie) getLargestArea() {

	this.parseGrid()
	borders := this.getBorder()
	this.bfs(borders)

	for i, coord1 := range this.tiles {
		for _, coord2 := range this.tiles[i+1:] {
			area := (abs(coord1.x-coord2.x) + 1) * (abs(coord1.y-coord2.y) + 1)
			this.part1 = max(this.part1, area)
			c1 := this.getGridCoord(coord1)
			c2 := this.getGridCoord(coord2)

			if this.isValid(c1, c2) {
				this.part2 = max(this.part2, area)
			}
		}
	}
}

func (this *Movie) getGridCoord(c Coord) Coord {
	return Coord{this.xLookup[c.x], this.yLookup[c.y]}
}

func (this *Movie) getPart1() int {
	return this.part1
}

func (this *Movie) getPart2() int {
	return this.part2
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()

	movie := &Movie{
		useTest: *useTest,
	}
	movie.getInput()
	movie.getLargestArea()
	fmt.Println("Day 9 part 1:", movie.getPart1())
	fmt.Println("Day 9 part 2:", movie.getPart2())
}
