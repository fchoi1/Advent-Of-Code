package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
	"strconv"
)

type Taxi struct {
	UseTest     bool
	Directions  [][]interface{}
	Position	[]int
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func (taxi *Taxi) getInput() {
	inputFile := "input.txt"
	if taxi.UseTest {
		inputFile = "input-test.txt"
	}

	data, err := ioutil.ReadFile(inputFile)
	if err != nil {
		log.Fatal(err)
	}

	line := strings.TrimSpace(string(data))
	parts := strings.Split(line, ", ")
	taxi.Directions = make([][]interface{}, len(parts))
	for i, part := range parts {
		direction := string(part[0])
		distanceStr := strings.TrimPrefix(part, direction)
		distance, _ := strconv.Atoi(strings.TrimSpace(distanceStr))
		taxi.Directions[i] = []interface{}{direction, distance}
	}
}

func (taxi *Taxi) getDistance() int {
	dirMap := map[string][2]int{
		"N": {0, 1},
		"S": {0, -1},
		"E": {1, 0},
		"W": {-1, 0},
	}
	dirStr := "NESW"
	currentDirIndex := 0

	for _, direction := range taxi.Directions {
		roatation := direction[0].(string)
    	steps := direction[1].(int) 

		if roatation == "R" {
			currentDirIndex = (currentDirIndex + 1) % len(dirStr)
		} else if roatation == "L" {
			currentDirIndex = (currentDirIndex - 1 + len(dirStr)) % len(dirStr)
		}
		currentDir := string(dirStr[currentDirIndex])
		movement := dirMap[currentDir]
		taxi.Position[0] += movement[0] * steps
		taxi.Position[1] += movement[1] * steps
	}
	return Abs(taxi.Position[0] ) +  Abs(taxi.Position[1])
}

func main() {
	taxi := &Taxi{
		UseTest:  false,
		Position: []int{0,0},
	}
	taxi.getInput()
	fmt.Println("Day 1 part 1:", taxi.getDistance())
	fmt.Println("Day 1 part 2:")
}