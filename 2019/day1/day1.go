package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"strconv"
)

type Rocket struct {
	UseTest     bool
	Directions  [][]interface{}
	Position	[]int
	first		[]int
}


func (rocket *Rocket) getInput() {
	inputFile := "input.txt"
	if rocket.UseTest {
		inputFile = "input-test.txt"
	}

	data, _ := ioutil.ReadFile(inputFile)
	line := strings.TrimSpace(string(data))
	parts := strings.Split(line, ", ")
	rocket.Directions = make([][]interface{}, len(parts))

	for i, part := range parts {
		direction := string(part[0])
		distanceStr := strings.TrimPrefix(part, direction)
		distance, _ := strconv.Atoi(strings.TrimSpace(distanceStr))
		rocket.Directions[i] = []interface{}{direction, distance}
	}
}

func (rocket *Rocket) travel(){
	seenMap := make(map[string]bool)
	dirMap := map[string][2]int{
		"N": {0, 1},
		"S": {0, -1},
		"E": {1, 0},
		"W": {-1, 0},
	}
	dirStr := "NESW"
	currentDirIndex := 0

	for _, direction := range rocket.Directions {
		roatation := direction[0].(string)
    	steps := direction[1].(int) 

		if roatation == "R" {
			currentDirIndex = (currentDirIndex + 1) % len(dirStr)
		} else if roatation == "L" {
			currentDirIndex = (currentDirIndex - 1 + len(dirStr)) % len(dirStr)
		}
		currentDir := string(dirStr[currentDirIndex])
		movement := dirMap[currentDir]
		
		for i := 0; i < steps; i++ {
			rocket.Position[0] += movement[0] 
			rocket.Position[1] += movement[1] 
			strKey := strconv.Itoa(rocket.Position[0]) + "," + strconv.Itoa(rocket.Position[1])
			if seenMap[strKey] && len(rocket.first) <= 0 {
				rocket.first = append(rocket.first, rocket.Position[0], rocket.Position[1])
			}
			seenMap[strKey] = true
		}
	}
}

func (rocket *Rocket) getDistance() int {
	return 1
}



func main() {
	rocket := &Rocket{
		UseTest:  false,
		Position: []int{0,0},
		first: []int{},
	}
	rocket.getInput()
	rocket.travel()
	fmt.Println("Day 1 part 1:", rocket.getDistance())
}