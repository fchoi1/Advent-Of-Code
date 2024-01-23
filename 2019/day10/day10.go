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

type Monitor struct {
	UseTest      bool
	rockMap      [][]rune
	asteroids    [][]int
	currAsteroid []int
	maxCount     int
	asteroid200  int
}

type AsteroidResult struct {
	count int
	seen  map[string][]int
}

func getDist(loc1, loc2 []int) int {
	return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func parseNumbers(key string) []float64 {
	parts := strings.Split(key, ",")
	num1, _ := strconv.ParseFloat(parts[0], 64)
	num2, _ := strconv.ParseFloat(parts[1], 64)
	return []float64{num2, num1}
}

func parseMap(locMap map[string][]int) [][]float64 {
	asteroidList := [][]float64{}
	for key, value := range locMap {
		parsed := parseNumbers(key)
		parsed = append(parsed, float64(value[0]), float64(value[1]))
		asteroidList = append(asteroidList, parsed)
	}
	sortFunc := func(i, j int) bool {
		if asteroidList[i][0] == asteroidList[j][0] {
			return asteroidList[i][1] < asteroidList[j][1]
		}
		return asteroidList[i][0] > asteroidList[j][0]
	}
	sort.Slice(asteroidList, sortFunc)
	return asteroidList
}

func parseAndReplaceInfinity(str string) int {
	if str == "+Inf" {
		return math.MaxInt
	} else if str == "-Inf" {
		return math.MinInt
	} else {
		num, _ := strconv.Atoi(str)
		return num
	}
}

func (this *Monitor) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.rockMap = append(this.rockMap, []rune(line))
	}
	this.asteroids = this.getAsteroids()
	defer file.Close()
}

func (this *Monitor) getAsteroids() [][]int {
	asteroids := [][]int{}
	for y, row := range this.rockMap {
		for x, val := range row {
			if val == '#' {
				asteroids = append(asteroids, []int{x, y})
			}
		}
	}
	return asteroids
}

func (this *Monitor) getVisible(currAsteroid []int) AsteroidResult {
	count := 0
	seen := make(map[string][]int)
	currX, currY := currAsteroid[0], currAsteroid[1]
	for _, asteroid := range this.asteroids {
		x, y := asteroid[0], asteroid[1]
		if x == currX && y == currY {
			continue
		}
		slope := float64(y-currY) / float64(x-currX)
		result := "0"
		if x > currX || (x == currX && y <= currY) {
			result = "1"
		}
		if math.IsInf(slope, 1) {
			slope = math.Inf(-1)
		}
		slopeStr := strconv.FormatFloat(slope, 'f', -1, 64)
		key := slopeStr + "," + result
		_, exists := seen[key]
		if !exists {
			count++
			seen[key] = asteroid
		}
		if getDist(currAsteroid, asteroid) < getDist(currAsteroid, seen[key]) {
			seen[key] = asteroid
		}
	}
	return AsteroidResult{count, seen}
}

func (this *Monitor) analyzeAsteroids() {
	maxCount := 0
	currAsteroid := []int{}
	destroyLimit := 200
	currSeen := make(map[string][]int)
	for _, asteroid := range this.asteroids {
		AR := this.getVisible(asteroid)
		if maxCount < AR.count {
			maxCount = AR.count
			currAsteroid = asteroid
			currSeen = AR.seen
		}
	}
	this.currAsteroid = currAsteroid
	this.maxCount = maxCount
	asteroidList := parseMap(currSeen)

	if len(asteroidList) < destroyLimit {
		fmt.Println("loop again") // Too lazy to implement
	} else {
		this.asteroid200 = int(asteroidList[destroyLimit-1][2]*100 + asteroidList[destroyLimit-1][3])
	}
}

func (this *Monitor) getMaxCount() int {
	return this.maxCount
}

func (this *Monitor) get200th() int {
	return this.asteroid200
}

func main() {
	monitor := &Monitor{
		UseTest: false,
	}
	monitor.getInput()
	monitor.analyzeAsteroids()
	fmt.Println("Day 9 part 1:", monitor.getMaxCount())
	fmt.Println("Day 9 part 2:", monitor.get200th())
}
