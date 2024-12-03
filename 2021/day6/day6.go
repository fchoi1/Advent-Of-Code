package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Hydrothermal struct {
	useTest   bool
	fishes    []int
	birth     int
	totalDays int
}

type point struct {
	x, y int
}

func (this *Hydrothermal) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Split(line, ",")
		for _, s := range splitted {
			n, _ := strconv.Atoi(s)
			this.fishes = append(this.fishes, n)
		}

	}
	this.birth = 7
	this.totalDays = 256
	if this.useTest {
		this.totalDays = 256
	}
	defer file.Close()
}

func (this *Hydrothermal) countSpawn(days int, remain int) int {
	if days < 7 || days < remain {
		return 0
	}
	days -= remain
	count := 1
	newFish := days / this.birth
	for i := 0; i <= newFish; i++ {
		count += this.countSpawn(days, 9)
		days -= this.birth

	}
	return count + newFish
}

func (this *Hydrothermal) countFish() int {
	var count int
	cache := make(map[int]int)
	for i, fish := range this.fishes {
		fmt.Println("here", i)
		count += this.countSpawn(this.totalDays, fish)
	}

	return count + len(this.fishes)
}

func main() {
	Hydrothermal := &Hydrothermal{
		useTest: false,
	}
	Hydrothermal.getInput()
	fmt.Println("Day 5 part 1:", Hydrothermal.countFish())
	fmt.Println("Day 5 part 2:", Hydrothermal.countFish())
}
