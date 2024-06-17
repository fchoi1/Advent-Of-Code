package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Bingo struct {
	useTest    bool
	numbers    []int
	Boards     [][][]int
	BoardsMap  []map[int][]int
	called     map[int]bool
	firstScore int
	lastScore  int
}

func convertRow(row string, delim string) []int {
	converted := []int{}
	var strSlice []string
	if delim == " " {
		strSlice = strings.Fields(row)
	} else {
		strSlice = strings.Split(row, delim)
	}
	for _, str := range strSlice {
		num, _ := strconv.Atoi(str)
		converted = append(converted, num)
	}
	return converted
}

func (this *Bingo) getInput() {
	inputFile := "input.txt"
	if this.useTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	currBoard := [][]int{}
	boardMap := map[int][]int{}
	this.called = make(map[int]bool)
	row := 0
	for scanner.Scan() {
		line := scanner.Text()
		if len(this.numbers) == 0 {
			this.numbers = convertRow(line, ",")
		} else {
			if line == "" && len(currBoard) > 0 {
				this.Boards = append(this.Boards, currBoard)
				this.BoardsMap = append(this.BoardsMap, boardMap)
				currBoard = [][]int{}
				boardMap = map[int][]int{}
				row = 0
			} else if line != "" {
				coverted := convertRow(line, " ")
				currBoard = append(currBoard, coverted)
				for x, val := range coverted {
					boardMap[val] = []int{x, row}
				}
				row++
			}
		}
	}
	this.Boards = append(this.Boards, currBoard)
	this.BoardsMap = append(this.BoardsMap, boardMap)
	defer file.Close()
}

func (this *Bingo) isBingo(board [][]int, x int, y int) bool {
	var row, col int
	for i := 0; i < 5; i++ {
		if _, exists := this.called[board[i][x]]; exists {
			row++
		}
		if _, exists := this.called[board[y][i]]; exists {
			col++
		}
	}
	return row == 5 || col == 5
}

func (this *Bingo) getSum(board [][]int) int {
	var sum int
	for _, row := range board {
		for _, val := range row {
			if _, exists := this.called[val]; !exists {
				sum += val
			}
		}
	}
	return sum
}

func (this *Bingo) getScore() {
	this.getInput()
	boardWin := make(map[int]bool)
	for _, n := range this.numbers {
		this.called[n] = true
		for i, boardMap := range this.BoardsMap {
			if coord, exists := boardMap[n]; exists {
				if this.isBingo(this.Boards[i], coord[0], coord[1]) {
					boardWin[i] = true
					if this.firstScore == 0 {
						this.firstScore = this.getSum(this.Boards[i]) * n
					}
					if len(boardWin) == len(this.Boards) {
						this.lastScore = this.getSum(this.Boards[i]) * n
						return
					}
				}
			}

		}
	}
}
func (this *Bingo) getFirstScore() int {
	return this.firstScore
}

func (this *Bingo) getLastScore() int {
	return this.lastScore
}

func main() {
	Bingo := &Bingo{
		useTest: false,
	}
	Bingo.getScore()
	fmt.Println("Day 4 part 1:", Bingo.getFirstScore())
	fmt.Println("Day 4 part 2:", Bingo.getLastScore())
}
