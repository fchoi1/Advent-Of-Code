package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
)

type Lab struct {
	useTest  bool
	manifold []string
	start    int
	splits   int
	paths    int
}

func (this *Lab) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.manifold = append(this.manifold, line)
	}
	defer file.Close()
	this.getStart()
}

func (this *Lab) getStart() {
	for i, val := range this.manifold[0] {
		if val == 'S' {
			this.start = i
			break
		}
	}
}

func (this *Lab) shootBeam() {
	beams := make(map[int]int)
	beams[this.start] = 1
	this.paths = 1
	for _, row := range this.manifold[1:] {
		newBeams := make(map[int]int)
		totalSplits := 0

		// Process one row
		for i, char := range row {
			if _, exists := beams[i]; !exists {
				continue
			}

			if char == '^' {
				this.splits += 1
				totalSplits += 1
				newBeams[i-1] += beams[i]
				newBeams[i+1] += beams[i]
				this.paths += beams[i]
			} else {
				newBeams[i] += beams[i]
			}
		}
		beams = newBeams
	}
}

func (this *Lab) getSplits() int {
	return this.splits
}
func (this *Lab) getPaths() int {
	return this.paths
}
func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()
	lab := &Lab{
		useTest: *useTest,
	}
	lab.getInput()
	lab.shootBeam()
	fmt.Println("Day 7 part 1:", lab.getSplits())
	fmt.Println("Day 7 part 2:", lab.getPaths())
}
