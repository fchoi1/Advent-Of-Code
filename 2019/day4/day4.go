package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Container struct {
	UseTest bool
	start   int
	end     int
}

func (this *Container) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		startStr, endStr := strings.Split(line, "-")[0], strings.Split(line, "-")[1]
		this.start, _ = strconv.Atoi(startStr)
		this.end, _ = strconv.Atoi(endStr)
	}
	defer file.Close()
}
func (w *Container) checkInput(n int, isPart2 bool) bool {
	strNum := strconv.Itoa(n)
	prevDigit, _ := strconv.Atoi(string(strNum[0]))
	sameCounter := 0
	same := false

	for _, char := range strNum[1:] {
		digit, _ := strconv.Atoi(string(char))

		if digit < prevDigit {
			return false
		}

		if digit == prevDigit {
			sameCounter++
		} else {
			if (isPart2 && sameCounter == 1) || (!isPart2 && sameCounter >= 1) {
				same = true
			}
			sameCounter = 0
		}
		prevDigit = digit
	}
	return (isPart2 && (same || sameCounter == 1)) || (!isPart2 && (same || sameCounter >= 1))
}

func (this *Container) countPasswords(isPart2 bool) int {
	start := max(100_000, this.start)
	end := min(999_999, this.end)
	count := 0
	for i := start; i <= end; i++ {
		if this.checkInput(i, isPart2) {
			count++
		}
	}
	return count
}

func main() {
	container := &Container{
		UseTest: false,
	}
	container.getInput()
	fmt.Println("Day 3 part 1:", container.countPasswords(false))
	fmt.Println("Day 3 part 1:", container.countPasswords(true))

}
