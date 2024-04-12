package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
)

type Rocket struct {
	UseTest bool
	Masses  []int
}

func (this *Rocket) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		mass, _ := strconv.Atoi(line)
		this.Masses = append(this.Masses, mass)
	}
	defer file.Close()
}

func (this *Rocket) getFuel(isPart2 bool) int {
	total := 0
	for _, num := range this.Masses {
		fuel := int(math.Floor(float64(num)/3) - 2)
		if isPart2 {
			for fuel > 0 {
				total += fuel
				fuel = int(math.Floor(float64(fuel)/3) - 2)
			}
		} else {
			total += fuel
		}
	}
	return total
}

func main() {
	rocket := &Rocket{
		UseTest: false,
		Masses:  []int{},
	}
	rocket.getInput()
	fmt.Println("Day 1 part 1:", rocket.getFuel(false))
	fmt.Println("Day 1 part 2:", rocket.getFuel(true))
}
