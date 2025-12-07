package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Cafeteria struct {
	useTest     bool
	fresh       []Range
	ingredients []int
}

type Range struct {
	start int
	end   int
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func (this *Cafeteria) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	isRange := true
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			isRange = false
		}

		if isRange {
			splitted := strings.Split(line, "-")
			start, _ := strconv.Atoi(splitted[0])
			end, _ := strconv.Atoi(splitted[1])
			this.fresh = append(this.fresh, Range{start, end})
		} else {
			val, _ := strconv.Atoi(line)
			this.ingredients = append(this.ingredients, val)
		}
	}
	defer file.Close()
}

func (this *Cafeteria) countFresh() int {
	count := 0

	for _, val := range this.ingredients {
		for _, r := range this.fresh {
			if val >= r.start && val <= r.end {
				count++
				break
			}
		}
	}
	return count
}

func (this *Cafeteria) countAllFresh() int {
	count := 0

	// sort by start
	slices.SortFunc(this.fresh, func(a, b Range) int {
		return a.start - b.start
	})

	var newRanges []Range

	for _, r := range this.fresh {
		if len(newRanges) == 0 {
			newRanges = append(newRanges, r)
		}

		if r.start <= newRanges[len(newRanges)-1].end {
			prev := newRanges[len(newRanges)-1]
			newRanges[len(newRanges)-1] = Range{
				start: min(prev.start, r.start),
				end:   max(prev.end, r.end),
			}
		} else {
			newRanges = append(newRanges, r)
		}
	}

	for _, r := range newRanges {
		count += r.end - r.start + 1
	}

	return count

}
func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()
	cafeteria := &Cafeteria{
		useTest: *useTest,
	}
	cafeteria.getInput()
	fmt.Println("Day 5 part 1:", cafeteria.countFresh())
	fmt.Println("Day 6 part 2:", cafeteria.countAllFresh())
}
