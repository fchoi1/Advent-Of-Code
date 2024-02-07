package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Jupiter struct {
	UseTest bool
	moons   []Moon
}

type Moon struct {
	position []int
	velocity []int
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func lcm(a, b int) int {
	return (a * b) / gcd(a, b)
}

func (this *Jupiter) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.moons = []Moon{}
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == '=' || r == ',' || r == '>'
		})
		x, _ := strconv.Atoi(splitted[1])
		y, _ := strconv.Atoi(splitted[3])
		z, _ := strconv.Atoi(splitted[5])
		newMoon := Moon{[]int{x, y, z}, []int{0, 0, 0}}
		this.moons = append(this.moons, newMoon)
	}
	defer file.Close()
}

func (this *Jupiter) updateVel(moon1 Moon, moon2 Moon) {
	for i := 0; i < 3; i++ {
		if moon1.position[i] > moon2.position[i] {
			moon1.velocity[i] -= 1
			moon2.velocity[i] += 1
		} else if moon2.position[i] > moon1.position[i] {
			moon1.velocity[i] += 1
			moon2.velocity[i] -= 1
		}
	}
}

func (this *Jupiter) updateMoons() {
	for i, moon1 := range this.moons[:len(this.moons)-1] {
		for _, moon2 := range this.moons[i+1:] {
			this.updateVel(moon1, moon2)
		}
	}
	for _, moon := range this.moons {
		for i := 0; i < 3; i++ {
			moon.position[i] += moon.velocity[i]
		}
	}
}

func (this *Jupiter) runSim() {
	totalSteps := 1000
	if this.UseTest {
		totalSteps = 100
	}
	for steps := 0; steps < totalSteps; steps++ {
		this.updateMoons()
	}
}

func (this *Jupiter) getEnergy() int {
	this.getInput()
	this.runSim()
	totalEnergy := 0
	for _, moon := range this.moons {
		pot := 0
		kin := 0
		for i := 0; i < 3; i++ {
			pot += abs(moon.position[i])
			kin += abs(moon.velocity[i])
		}
		totalEnergy += pot * kin
	}
	return totalEnergy
}

func (this *Jupiter) allSeen(isSeen []int) bool {
	for _, seen := range isSeen {
		if seen == 0 {
			return false
		}
	}
	return true
}

func (this *Jupiter) getStrKey() []string {
	keys := make([]string, 3)
	for _, moon := range this.moons {
		keys[0] += strconv.Itoa(moon.position[0]) + "," + strconv.Itoa(moon.velocity[0]) + ","
		keys[1] += strconv.Itoa(moon.position[1]) + "," + strconv.Itoa(moon.velocity[1]) + ","
		keys[2] += strconv.Itoa(moon.position[2]) + "," + strconv.Itoa(moon.velocity[2]) + ","
	}
	return keys
}

func (this *Jupiter) getLoop() int {
	this.getInput()
	loops := []int{0, 0, 0}
	initial := this.getStrKey()
	visitedList := make([]map[string]bool, 4)
	for i := range visitedList {
		visitedList[i] = make(map[string]bool)
	}
	step := 0
	for {
		step += 1
		this.updateMoons()
		strKeys := this.getStrKey()
		for i := 0; i < 3; i++ {
			if loops[i] == 0 && strKeys[i] == initial[i] {
				loops[i] = step
			}
		}
		if this.allSeen(loops) {
			break
		}
	}
	return lcm(lcm(loops[0], loops[1]), loops[2])
}

func main() {
	jupiter := &Jupiter{
		UseTest: false,
	}
	fmt.Println("Day 12 part 1:", jupiter.getEnergy())
	fmt.Println("Day 12 part 2:", jupiter.getLoop())
}
