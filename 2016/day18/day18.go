package main

import (
	"bufio"
	"fmt"
	"os"
)

type Trap struct {
	UseTest  bool
	startRow string
}

func (this *Trap) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.startRow = scanner.Text()
	}
	defer file.Close()
}

func isTrap(target string) bool {
	trapList := []string{"^^.", ".^^", "^..", "..^"}
	for _, item := range trapList {
		if item == target {
			return true
		}
	}
	return false
}

func (this *Trap) getSafeTiles(isPart2 bool) int {
	var rows int
	if this.UseTest {
		rows = 9
	} else {
		rows = 39
	}
	if isPart2 {
		rows = 400_000 - 1
	}
	prevRow := this.startRow
	safeTiles := 0
	N := len(this.startRow)
	for _, tile := range this.startRow {
		if tile == '.' {
			safeTiles++
		}
	}
	for i := 0; i < rows; i++ {
		newRow := ""
		for j := 0; j < N; j++ {
			strMatch := ""
			if j-1 < 0 {
				strMatch = "." + prevRow[j:j+2]
			} else if j+1 >= N {
				strMatch = prevRow[j-1:j+1] + "."
			} else {
				strMatch = prevRow[j-1 : j+2]
			}
			if isTrap(strMatch) {
				newRow += "^"
			} else {
				newRow += "."
				safeTiles++
			}
		}
		prevRow = newRow
	}
	return safeTiles
}

func main() {
	trap := &Trap{
		UseTest: false,
	}
	trap.getInput()
	fmt.Println("Day 18 part 1:", trap.getSafeTiles(false))
	fmt.Println("Day 18 part 2:", trap.getSafeTiles(true))
	// Total Runtime ~2s
}
