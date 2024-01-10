package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Orbits struct {
	UseTest     bool
	orbitMap    map[string][]string
	orbitMapDir map[string][]string
	totalOrbits int
}

func (this *Orbits) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.orbitMap = make(map[string][]string)
	this.orbitMapDir = make(map[string][]string)
	for scanner.Scan() {
		line := scanner.Text()
		orbitEntry := strings.Split(line, ")")
		this.orbitMap[orbitEntry[0]] = append(this.orbitMap[orbitEntry[0]], orbitEntry[1])
		this.orbitMapDir[orbitEntry[0]] = append(this.orbitMapDir[orbitEntry[0]], orbitEntry[1])
		this.orbitMapDir[orbitEntry[1]] = append(this.orbitMapDir[orbitEntry[1]], orbitEntry[0])
	}
	defer file.Close()
}

func (this *Orbits) arithmeticSum(n int) int {
	return n * (1 + n) / 2
}

func (this *Orbits) countChild(node string, count int) int {
	nodes, exists := this.orbitMap[node]
	if !exists {
		return count
	}
	for _, node := range nodes {
		nodeCount := this.countChild(node, count+1)
		this.totalOrbits += nodeCount
	}
	return count
}
func (this *Orbits) countOrbits() int {
	this.countChild("COM", 0)
	return this.totalOrbits
}

func (this *Orbits) bfs(start string, target string) int {
	q, seen, steps := []string{start}, make(map[string]bool), 0
	for len(q) > 0 {
		temp := []string{}
		for _, node := range q {
			_, exists := seen[node]
			if node == target {
				return steps
			}
			if exists {
				continue
			}
			seen[node] = true
			temp = append(temp, this.orbitMapDir[node]...)
		}
		steps++
		q = temp
	}
	return -1
}

func (this *Orbits) findMinOrbit() int {
	return this.bfs("YOU", "SAN") - 2
}

func main() {
	orbits := &Orbits{
		UseTest:     false,
		totalOrbits: 0,
	}
	orbits.getInput()
	fmt.Println("Day 6 part 1:", orbits.countOrbits())
	fmt.Println("Day 6 part 2:", orbits.findMinOrbit())
}
