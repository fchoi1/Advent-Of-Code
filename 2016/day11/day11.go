package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strings"
)

type Elevator struct {
	UseTest      bool
	Elevator     string
	Floors       map[int]Floor
	steps        int
	permutations []string
}
type Floor struct {
	id    int
	gens  []string
	chips []string
}

func (this *Elevator) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	floor := 1
	this.Floors = make(map[int]Floor)
	for scanner.Scan() {
		line := scanner.Text()

		newFloor := Floor{
			id:    floor,
			gens:  []string{},
			chips: []string{},
		}
		if floor == 4 {
			this.Floors[floor] = newFloor
			continue
		}
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == ' ' || r == ',' || r == '.'
		})[5:]
		indexToRemove := len(splitted) - 4
		splitted = append(splitted[:indexToRemove], splitted[indexToRemove+1:]...)

		var name string
		for i, word := range splitted {
			if i%3 == 0 {
				name = word[:2]
			}
			if i%3 == 1 {
				if word == "generator" {
					newFloor.gens = append(newFloor.gens, name)
				} else if word == "microchip" {
					newFloor.chips = append(newFloor.chips, name)
					this.permutations = append(this.permutations, name)
				}
			}
		}
		sort.Strings(newFloor.gens)
		sort.Strings(newFloor.chips)
		this.Floors[floor] = newFloor
		floor++
	}
	fmt.Println(this)
	defer file.Close()
}

func generatePermutations(input []string, start int, result *[][]string) {
	if start == len(input) {
		*result = append(*result, append([]string(nil), input...))
		return
	}
	for i := start; i < len(input); i++ {
		input[start], input[i] = input[i], input[start]
		generatePermutations(input, start+1, result)
		input[start], input[i] = input[i], input[start]
	}
}

func permutations(input []string) [][]string {
	var result [][]string
	generatePermutations(input, 0, &result)
	return result
}

func getItems(floor Floor) []string {
	var str []string
	// check items, can move one at a time, or both,  unless

	// if there are multiple pairs, doesnt matter which item in pair

	return str
}

func checkElevator(elevator Elevator, floorId int) (bool, bool) {
	allDone := true
	for floorNum, floor := range elevator.Floors {
		lookup := make(map[string]bool)
		if floorNum != 4 && (len(floor.chips) != 0 || len(floor.gens) != 0) {
			allDone = false
		}
		for _, gen := range floor.gens {
			lookup[gen] = true
		}
		for _, chip := range floor.chips {
			_, exists := lookup[chip]
			if !exists {
				return false, false
			}
		}
	}
	return true, allDone
}

func isRepeat(elevator Elevator, visited map[string]bool) bool {
	length := len(elevator.permutations)
	perms := permutations(elevator.permutations)
	var strKey string
	// 5 objects = 120 permutations
	// 6 objects = 720 permutations
	for _, permutation := range perms {
		strKey = ""
		tempGen := []string{}
		tempChip := []string{}
		permMap := make(map[string]string)

		for i := 0; i < length; i++ {
			permMap[elevator.permutations[i]] = permutation[i]
		}
		for _, floor := range elevator.Floors {
			for _, chip := range floor.chips {
				tempChip = append(tempChip, permMap[chip])
			}
			for _, gen := range floor.gens {
				tempGen = append(tempGen, permMap[gen])
			}
		}
		sort.Strings(tempGen)
		sort.Strings(tempChip)
		chipStr := strings.Join(tempChip, ",")
		genStr := strings.Join(tempGen, ",")
		strKey += chipStr + "-" + genStr + ":"

		_, exists := visited[strKey]
		if exists {
			return true
		}
		visited[strKey] = true
	}
	return false
}

func removeElement(slice []string, element string) []string {
	var updatedSlice []string
	for _, value := range slice {
		if value != element {
			updatedSlice = append(updatedSlice, value)
		}
	}
	return updatedSlice
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func moveChips(items []string, floorId int, elevator Elevator, steps int, visited map[string]bool) int {
	minSteps := math.MaxInt64
	isRepeat := isRepeat(elevator, visited)
	if isRepeat {
		return minSteps
	}

	currentFloor := elevator.Floors[floorId]

	for _, item := range items { // put items in floor and check
		itemType, name := strings.Split(item, "-")[0], strings.Split(item, "-")[1]
		if itemType == "g" {
			currentFloor.gens = append(currentFloor.gens, name)
		} else {
			currentFloor.chips = append(currentFloor.chips, name)
		}
	}

	chipInGen, allDone := checkElevator(elevator, floorId)

	if !chipInGen {
		return minSteps
	}
	if allDone {
		return steps
	}
	return minSteps
}

func (this *Elevator) getMinSteps() int {
	return this.steps
}

func main() {
	elevator := &Elevator{
		UseTest: false,
	}
	elevator.getInput()
	fmt.Println("Day 11 part 1:", elevator.getMinSteps())
	// fmt.Println("Day 11 part 2:", Elevator.getProduct())
}
