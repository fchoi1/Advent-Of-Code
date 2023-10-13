package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Elevator struct {
	UseTest      bool
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
		if len(splitted) > 3 {
			indexToRemove := len(splitted) - 4
			splitted = append(splitted[:indexToRemove], splitted[indexToRemove+1:]...)
		}
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
	defer file.Close()
}

func deepCopyFloor(src Floor) Floor {
	dest := Floor{
		id: src.id,
	}
	dest.gens = make([]string, len(src.gens))
	copy(dest.gens, src.gens)
	dest.chips = make([]string, len(src.chips))
	copy(dest.chips, src.chips)
	return dest
}

func generatePermutations(items []string) [][]string {
	var result [][]string
	var generate func(int, []string)
	generate = func(n int, items []string) {
		if n == 1 {
			result = append(result, append([]string(nil), items...))
			return
		}
		for i := 0; i < n; i++ {
			generate(n-1, items)
			if n%2 == 0 {
				items[i], items[n-1] = items[n-1], items[i]
			} else {
				items[0], items[n-1] = items[n-1], items[0]
			}
		}
	}
	generate(len(items), items)
	return result
}
func permutations(input []string) [][]string {
	return generatePermutations(input)
}

func generatePairs(items []string) [][]string {
	var result [][]string
	var generate func(int, []string)
	generate = func(start int, current []string) {
		if len(current) == 2 {
			result = append(result, append([]string(nil), current...))
			return
		}
		for i := start; i < len(items); i++ {
			generate(i+1, append(current, items[i]))
		}
	}
	generate(0, []string{})
	return result
}

func getItems(floor Floor) [][]string {
	var itemList []string
	for _, chip := range floor.chips {
		itemList = append(itemList, "c-"+chip)
	}
	for _, gen := range floor.gens {
		itemList = append(itemList, "g-"+gen)
	}
	movableItems := generatePairs(itemList)
	for _, str := range itemList {
		movableItems = append(movableItems, []string{str})
	}
	return movableItems
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
			if !exists && len(lookup) > 0 {
				return false, false
			}
		}
	}
	return true, allDone
}

func generateKey(elevator Elevator, strKey string, useMap bool, permMap map[string]string) string {
	for i := 1; i <= 4; i++ {
		floor := elevator.Floors[i]
		tempGen := []string{}
		tempChip := []string{}
		for _, chip := range floor.chips {
			if useMap {
				tempChip = append(tempChip, permMap[chip])
			} else {
				tempChip = append(tempChip, chip)
			}
		}
		for _, gen := range floor.gens {
			if useMap {
				tempGen = append(tempGen, permMap[gen])
			} else {
				tempGen = append(tempGen, gen)
			}
		}
		sort.Strings(tempGen)
		sort.Strings(tempChip)
		chipStr := strings.Join(tempChip, ",")
		genStr := strings.Join(tempGen, ",")
		strKey += chipStr + "-" + genStr + ":"
	}
	return strKey
}

func isRepeat(floor int, elevator Elevator, visited map[string]int, step int) bool {
	length := len(elevator.permutations)
	perms := permutations(elevator.permutations)
	key := generateKey(elevator, strconv.Itoa(floor)+":", false, make(map[string]string))
	visitedStep, exists := visited[key]
	if exists && step >= visitedStep {
		return true
	} else if exists {
		visited[key] = step
	}
	// 5 objects = 120 permutations
	// 6 objects = 720 permutations
	for _, permutation := range perms {
		permMap := make(map[string]string)
		strKey := strconv.Itoa(floor) + ":"

		for i := 0; i < length; i++ {
			permMap[elevator.permutations[i]] = permutation[i]
		}
		strKey = generateKey(elevator, strKey, true, permMap)
		visited[strKey] = step
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

func deepCopyBoolMap(originalMap map[string]bool) map[string]bool {
	copiedMap := make(map[string]bool)
	for key, value := range originalMap {
		copiedMap[key] = value
	}
	return copiedMap
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func (this *Elevator) moveChips(items []string, floorId int, elevator Elevator, steps int, visited map[string]int) {
	if steps > 500 || steps > this.steps {
		// fmt.Println("pasted steps", steps)
		return
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
	elevator.Floors[floorId] = currentFloor

	chipInGen, allDone := checkElevator(elevator, floorId)
	// fmt.Println("step", steps, "FLOOR", floorId, "Elevator after", elevator)

	if !chipInGen {
		// fmt.Println("chipInGen", elevator, steps)
		return
	}
	if allDone {
		this.steps = min(this.steps, steps)
		// fmt.Println("DONE this", steps, "this", elevator)
		return
	}

	isRepeat := isRepeat(floorId, elevator, visited, steps)

	if isRepeat {
		// fmt.Println("isRepeat", elevator, steps)
		return
	}

	movableItems := getItems(currentFloor)
	for _, newFloorId := range []int{floorId + 1, floorId - 1} {
		if newFloorId < 1 || newFloorId > 4 {
			continue
		}
		for _, items := range movableItems {
			newElevator := Elevator{
				UseTest:      elevator.UseTest,
				steps:        elevator.steps,
				permutations: make([]string, len(elevator.permutations)),
				Floors:       make(map[int]Floor),
			}
			copy(newElevator.permutations, elevator.permutations)
			for key, floor := range elevator.Floors {
				newElevator.Floors[key] = deepCopyFloor(floor)
			}
			newFloor := newElevator.Floors[floorId]

			for _, item := range items {
				itemType, name := strings.Split(item, "-")[0], strings.Split(item, "-")[1]
				if itemType == "g" {
					newFloor.gens = removeElement(newFloor.gens, name)
				} else {
					newFloor.chips = removeElement(newFloor.chips, name)
				}
				// fmt.Println(floorId, "newFloor after", newFloor)
			}
			newElevator.Floors[floorId] = newFloor
			// fmt.Println("calling again", newFloorId, newElevator.Floors, items, "steps", steps)
			this.moveChips(items, newFloorId, newElevator, steps+1, visited)
		}
	}

}

func (this *Elevator) getMinSteps(isPart2 bool) int {
	this.steps = math.MaxInt64
	elevator := *this

	if isPart2 {
		floor := elevator.Floors[1]
		floor.gens = append(floor.gens, "el", "di")
		floor.chips = append(floor.chips, "el", "di")
		elevator.permutations = append(elevator.permutations, "el", "di")
		elevator.Floors[1] = floor
	}
	fmt.Println(elevator.Floors)

	this.moveChips([]string{}, 1, elevator, 0, make(map[string]int))
	fmt.Println("fin", this)
	return this.steps
}

func main() {
	elevator := &Elevator{
		UseTest: false,
		steps:   math.MaxInt64,
	}
	elevator.getInput()
	fmt.Println("Day 11 part 1:", elevator.getMinSteps(false))
	// fmt.Println("Day 11 part 2:", elevator.getMinSteps(true))

	// fmt.Println("Day 11 part 2:", Elevator.getProduct())
}
