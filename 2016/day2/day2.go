package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Bathroom struct {
	UseTest  bool
	Input    [][]string
	Password string
}

func (this *Bathroom) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		this.Input = append(this.Input, strings.Split(line, ""))
	}
	defer file.Close()
}

func (this *Bathroom) findPassword(isPart2 bool) {
	var numPad [][]string
	var posX, posY int
	if isPart2 {
		numPad = [][]string{
			{".", ".", "1", ".", "."},
			{".", "2", "3", "4", "."},
			{"5", "6", "7", "8", "9"},
			{".", "A", "B", "C", "."},
			{".", ".", "D", ".", "."},
		}
		posX, posY = 0, 2
	} else {
		numPad = [][]string{
			{"1", "2", "3"},
			{"4", "5", "6"},
			{"7", "8", "9"},
		}
		posX, posY = 1, 1
	}
	dirMap := map[string][2]int{
		"U": {0, -1},
		"D": {0, 1},
		"R": {1, 0},
		"L": {-1, 0},
	}
	this.Password = ""

	for _, code := range this.Input {
		for _, dir := range code {
			move, exists := dirMap[dir]
			if exists {
				newX, newY := posX+move[0], posY+move[1]
				if newX >= 0 && newX < len(numPad) && newY >= 0 && newY < len(numPad[0]) &&
					numPad[newX][newY] != "." {
					posX, posY = newX, newY
				}
			}
		}
		this.Password += numPad[posY][posX]
	}
}

func (this *Bathroom) getPassword() string {
	this.findPassword(false)
	return this.Password
}

func (this *Bathroom) getPassword2() string {
	this.findPassword(true)
	return this.Password
}

func main() {
	bathroom := &Bathroom{
		UseTest: false,
	}
	bathroom.getInput()
	fmt.Println("Day 2 part 1:", bathroom.getPassword())
	fmt.Println("Day 2 part 1:", bathroom.getPassword2())
}
