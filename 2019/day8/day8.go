package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Image struct {
	UseTest bool
	layers  [][][]int
	data    string
	width   int
	height  int
}

func intListToString(numbers []int) string {
	strNumbers := make([]string, len(numbers))
	for i, num := range numbers {
		if num == 1 {
			strNumbers[i] = "# "
		} else {
			strNumbers[i] = "  "
		}
	}
	return strings.Join(strNumbers, "")
}

func (this *Image) getInput() {
	inputFile := "input.txt"
	this.width = 25
	this.height = 6
	if this.UseTest {
		inputFile = "input-test.txt"
		this.width = 2
		this.height = 2
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.data = strings.TrimSpace(scanner.Text())
	}
	this.formatLayers()
	defer file.Close()
}

func (this *Image) formatLayers() {
	slice := this.width * this.height
	this.layers = make([][][]int, 0)
	loops := len(this.data) / slice
	for i := 0; i < loops; i++ {
		layer := make([][]int, 0)
		for y := 0; y < this.height; y++ {
			row := make([]int, 0)
			for x := 0; x < this.width; x++ {
				val, _ := strconv.Atoi(string(this.data[i*slice+y*this.width+x]))
				row = append(row, val)
			}
			layer = append(layer, row)
		}
		this.layers = append(this.layers, layer)
	}
}

func (this *Image) getOutput() int {
	maxCount := math.MaxInt64
	maxLayer := 0
	for i := range this.layers {
		count := this.getCount(i, 0)
		if count < maxCount {
			maxCount = count
			maxLayer = i
		}
	}
	return this.getCount(maxLayer, 1) * this.getCount(maxLayer, 2)
}

func (this *Image) getCount(layer int, val int) int {
	count := 0
	for _, row := range this.layers[layer] {
		for _, n := range row {
			if n == val {
				count++
			}
		}
	}
	return count
}

func (this *Image) printImage() {
	image := this.layers[0]
	for _, layers := range this.layers[1:] {
		for y, row := range layers {
			for x, val := range row {
				if image[y][x] != 2 {
					continue
				}
				image[y][x] = val
			}
		}
	}
	for _, row := range image {
		fmt.Println(intListToString(row))
	}
}

func main() {
	image := &Image{
		UseTest: false,
	}
	image.getInput()
	fmt.Println("Day 8 part 1:", image.getOutput())
	fmt.Println("Day 8 part 2:")
	image.printImage()

}
