package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type GiftShop struct {
	useTest bool
	ranges  []Range
	part1   int
	part2   int
}

type Range struct {
	start int
	end   int
}

func mod(a, b int) int {
	return (a%b + b) % b
}

func (this *GiftShop) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		stringRanges := strings.Split(line, ",")
		for _, stringRange := range stringRanges {
			if stringRange == "" {
				break
			}
			splitted := strings.Split(stringRange, "-")
			start, _ := strconv.Atoi(splitted[0])
			end, _ := strconv.Atoi(splitted[1])
			this.ranges = append(this.ranges, Range{start, end})
		}
	}

	defer file.Close()
}

func invalidPart1(num int) bool {
	strNum := strconv.Itoa(num)
	l := len(strNum)
	return strNum[:l/2] == strNum[l/2:]
}

func invalidPart2(num int) bool {
	strNum := strconv.Itoa(num)
	N := len(strNum)
	curr := ""

	for i := 0; i < N/2; i++ {
		curr += string(strNum[i])

		// Check for repeats if divisible
		if mod(N, len(curr)) == 0 {
			times := N / len(curr)
			if strings.Count(strNum, curr) == times {
				return true
			}
		}

	}

	return false
}

func (this *GiftShop) parseIDs() {
	this.part1 = 0
	this.part2 = 0
	for _, r := range this.ranges {

		for i := r.start; i <= r.end; i++ {
			if invalidPart1(i) {
				this.part1 += i
			}
			if invalidPart2(i) {
				this.part2 += i
			}
		}
	}

}

func (this *GiftShop) getPart1() int {
	return this.part1
}

func (this *GiftShop) getPart2() int {
	return this.part2
}

func main() {
	useTest := flag.Bool("test", false, "use test input file")
	flag.Parse()

	giftShop := &GiftShop{
		useTest: *useTest,
	}
	giftShop.getInput()
	giftShop.parseIDs()
	fmt.Println("Day 2 part 1:", giftShop.getPart1())
	fmt.Println("Day 2 part 2:", giftShop.getPart2())
}
