package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Triangle struct {
	UseTest         bool
	Triangles       [][]int
	Triangles2      [][]int
	validTriangles  int
	validTriangles2 int
}

func sortNum(nums []int) []int {
	sort.Slice(nums, func(i, j int) bool {
		return nums[i] < nums[j]
	})
	return nums
}

func (this *Triangle) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)

	scanner := bufio.NewScanner(file)
	i := 0

	var tri1, tri2, tri3 []int

	for scanner.Scan() {
		line := scanner.Text()
		i++
		var intRow []int
		for _, strNum := range strings.Fields(line) {
			num, _ := strconv.Atoi(strNum)
			intRow = append(intRow, num)
		}
		tri1 = append(tri1, intRow[0])
		tri2 = append(tri2, intRow[1])
		tri3 = append(tri3, intRow[2])
		if i%3 == 0 {
			this.Triangles2 = append(this.Triangles2, sortNum(tri1))
			this.Triangles2 = append(this.Triangles2, sortNum(tri2))
			this.Triangles2 = append(this.Triangles2, sortNum(tri3))
			tri1, tri2, tri3 = []int{}, []int{}, []int{}
		}
		sortNum(intRow)
		this.Triangles = append(this.Triangles, intRow)
	}
	defer file.Close()
}

func (this *Triangle) checkTriangle() {

	this.validTriangles = 0
	this.validTriangles2 = 0

	for i := 0; i < len(this.Triangles); i++ {
		if this.Triangles[i][0]+this.Triangles[i][1] > this.Triangles[i][2] {
			this.validTriangles += 1
		}
		if this.Triangles2[i][0]+this.Triangles2[i][1] > this.Triangles2[i][2] {
			this.validTriangles2 += 1
		}
	}

}

func (this *Triangle) getPossibleTriangle(isPart2 bool) int {
	if isPart2 {
		return this.validTriangles2
	}
	return this.validTriangles
}

func main() {
	triangle := &Triangle{
		UseTest: false,
	}
	triangle.getInput()
	triangle.checkTriangle()
	fmt.Println("Day 3 part 1:", triangle.getPossibleTriangle(false))
	fmt.Println("Day 3 part 2:", triangle.getPossibleTriangle(true))
}
