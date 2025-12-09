package main

import (
	"bufio"
	"flag"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Boxes struct {
	useTest   bool
	junctions []Coord
	times     int
	part1     int
	part2     int
	// Union Find
	parent map[Coord]Coord
	size   map[Coord]int
}

type Coord struct {
	x int
	y int
	z int
}

type Dist struct {
	distance float64
	n1       Coord
	n2       Coord
}

func (c Coord) Sub(other Coord) Coord {
	return Coord{
		x: c.x - other.x,
		y: c.y - other.y,
		z: c.z - other.z,
	}
}

func (this *Boxes) getInput() {
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
		z, _ := strconv.Atoi(nums[2])
		this.junctions = append(this.junctions, Coord{x, y, z})
	}
	defer file.Close()
}

func getDist(junctions []Coord) []Dist {
	dist := []Dist{}

	for i, node1 := range junctions {
		for _, node2 := range junctions[i+1:] {
			diff := node1.Sub(node2)
			d := math.Sqrt(float64(diff.x*diff.x + diff.y*diff.y + diff.z*diff.z))
			dist = append(dist, Dist{d, node1, node2})
		}
	}
	sort.Slice(dist, func(i, j int) bool {
		return dist[i].distance < dist[j].distance
	})

	return dist
}

// Union Find implementation
func (this *Boxes) find(d Coord) Coord {
	if this.parent[d] != d {
		this.parent[d] = this.find(this.parent[d])
	}
	return this.parent[d]
}

func (this *Boxes) union(d1, d2 Coord) bool {

	p1 := this.find(d1)
	p2 := this.find(d2)

	s1 := this.size[p1]
	s2 := this.size[p2]

	if p1 == p2 {
		return false
	}
	if s1 < s2 {
		this.parent[p1] = p2
		this.size[p2] += this.size[p1]
		this.size[p1] = 0
	} else {
		this.parent[p2] = p1
		this.size[p1] += this.size[p2]
		this.size[p2] = 0
	}
	return true
}

func (this *Boxes) initUnionFind() {
	this.parent = make(map[Coord]Coord)
	this.size = make(map[Coord]int)

	for _, d := range this.junctions {
		this.parent[d] = d
		this.size[d] = 1
	}
}

func (this *Boxes) calcPart1() {
	sizes := []int{}
	for _, v := range this.size {
		if v == 0 {
			continue
		}
		sizes = append(sizes, v)
	}
	sort.Slice(sizes, func(i, j int) bool {
		return sizes[i] > sizes[j]
	})
	ans := 1
	for _, n := range sizes[:3] {
		ans *= n
	}
	this.part1 = ans
}

func (this *Boxes) connect() {
	var count int
	N := len(this.junctions)

	this.initUnionFind()
	dist := getDist(this.junctions)

	for _, d := range dist {
		if count == this.times {
			this.calcPart1()
		}
		count += 1
		if !this.union(d.n1, d.n2) {
			continue
		}
		if this.size[this.find(d.n1)] == N {
			this.part2 = d.n1.x * d.n2.x
			break
		}
	}
}

func (this *Boxes) getPart1() int {
	return this.part1
}

func (this *Boxes) getPart2() int {
	return this.part2
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()
	var n int
	if *useTest {
		n = 10
	} else {
		n = 1000
	}
	boxes := &Boxes{
		useTest: *useTest,
		times:   n,
	}
	boxes.getInput()
	boxes.connect()
	fmt.Println("Day 8 part 1:", boxes.getPart1())
	fmt.Println("Day 8 part 2:", boxes.getPart2())
}
