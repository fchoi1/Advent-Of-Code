package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Computer struct {
	UseTest   bool
	Blacklist [][]int
	Lowest    int
	BLcount   int
}

func (this *Computer) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.Blacklist = [][]int{}
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == '-'
		})
		num1, _ := strconv.Atoi(splitted[0])
		num2, _ := strconv.Atoi(splitted[1])
		this.Blacklist = append(this.Blacklist, []int{num1, num2})
	}
	defer file.Close()
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

func (this *Computer) blacklistIPs() {
	sort.Slice(this.Blacklist, func(i, j int) bool {
		if this.Blacklist[i][0] != this.Blacklist[j][0] {
			return this.Blacklist[i][0] < this.Blacklist[j][0]
		}
		return this.Blacklist[i][1] < this.Blacklist[j][1]
	})

	index := 0
	intervals := [][]int{this.Blacklist[0]}

	for _, IPrange := range this.Blacklist[1:] {
		currInterval := intervals[index]
		if IPrange[0] > currInterval[1]+1 {
			intervals = append(intervals, IPrange)
			index++
			continue
		}
		currInterval[0] = min(currInterval[0], IPrange[0])
		currInterval[1] = max(currInterval[1], IPrange[1])
		intervals[index] = currInterval
	}

	lowest := 0
	diff := 0
	lowestFound := false
	for _, interval := range intervals {
		if lowest >= interval[0] && lowest <= interval[1] && !lowestFound {
			lowest = interval[1] + 1
		} else {
			lowestFound = true
		}
		diff += interval[1] - interval[0] + 1
	}
	this.Lowest = lowest
	this.BLcount = 4294967296 - diff
}

func (this *Computer) getLowestIP() int {
	return this.Lowest
}

func (this *Computer) getBlacklistCount() int {
	return this.BLcount
}
func main() {
	computer := &Computer{
		UseTest: false,
	}
	computer.getInput()
	computer.blacklistIPs()
	fmt.Println("Day 19 part 1:", computer.getLowestIP())
	fmt.Println("Day 19 part 2:", computer.getBlacklistCount())
}
