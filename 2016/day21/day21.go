package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Scramble struct {
	UseTest   bool
	Commands  [][]string
	charList  []rune
	rotateMap map[int]int
}

func (this *Scramble) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.Commands = [][]string{}
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Fields(line)

		command := splitted[0]
		var commandStr []string
		if command == "swap" || command == "move" {
			commandStr = []string{command, splitted[2], splitted[5]}
		} else if command == "reverse" {
			commandStr = []string{command, splitted[2], splitted[4]}
		} else if command == "rotate" {

			if splitted[1] == "based" {
				commandStr = []string{command, "right", splitted[6]}
			} else {
				commandStr = []string{command, splitted[1], splitted[2]}
			}
		}
		this.Commands = append(this.Commands, commandStr)
	}
	defer file.Close()
}
func (this *Scramble) makeRotateMap() {
	this.rotateMap = make(map[int]int)
	N := len(this.charList)
	for i := 0; i < N; i++ {
		val := i*2 + 1
		if i >= 4 {
			val++
		}
		val %= N
		this.rotateMap[val] = i
	}
}
func reverseSlice(slice []rune) {
	for i, j := 0, len(slice)-1; i < j; i, j = i+1, j-1 {
		slice[i], slice[j] = slice[j], slice[i]
	}
}

func (this *Scramble) getIndex(c rune) int {
	for i, char := range this.charList {
		if char == c {
			return i
		}
	}
	return -1
}

func (this *Scramble) swap(x string, y string) {
	i, err1 := strconv.Atoi(x)
	j, err2 := strconv.Atoi(y)
	if err1 != nil || err2 != nil {
		i = this.getIndex(rune(x[0]))
		j = this.getIndex(rune(y[0]))
	}
	this.charList[i], this.charList[j] = this.charList[j], this.charList[i]
}

func (this *Scramble) move(x string, y string) {
	old, _ := strconv.Atoi(x)
	new, _ := strconv.Atoi(y)
	// Remove
	char := this.charList[old]
	this.charList = append(this.charList[:old], this.charList[old+1:]...)
	// Re add space and shift
	this.charList = append(this.charList, 0)
	copy(this.charList[new+1:], this.charList[new:])
	this.charList[new] = char
}

func (this *Scramble) reverse(x string, y string) {
	start, _ := strconv.Atoi(x)
	end, _ := strconv.Atoi(y)
	subset := this.charList[start : end+1]
	reverseSlice(subset)
	this.charList = append(append(this.charList[:start], subset...), this.charList[end+1:]...)
}

func (this *Scramble) rotate(dir string, unit string, reverse bool) {
	val, err1 := strconv.Atoi(unit)
	if err1 != nil {
		val = this.getIndex(rune(unit[0]))
		if reverse {
			val = val - this.rotateMap[val]
		} else {
			if val >= 4 && !reverse {
				val++
			}
			val++
		}
	}
	if dir == "right" {
		val = -val
	}
	val = val % len(this.charList)
	if val < 0 {
		val += len(this.charList)
	}
	this.charList = []rune((string(this.charList) + string(this.charList))[val : val+len(this.charList)])
}

func (this *Scramble) scramble(str string, unscramble bool) {
	if this.UseTest && !unscramble {
		str = "abcde"
	} else if this.UseTest {
		str = "decab"
	}
	this.charList = []rune(str)
	this.makeRotateMap()
	var operation []string
	for i := 0; i < len(this.Commands); i++ {
		if unscramble {
			operation = this.Commands[len(this.Commands)-1-i]
		} else {
			operation = this.Commands[i]
		}
		command := operation[0]
		if command == "swap" {
			this.swap(operation[1], operation[2])
		} else if command == "move" {
			if unscramble {
				this.move(operation[2], operation[1])
			} else {
				this.move(operation[1], operation[2])
			}
		} else if command == "reverse" {
			this.reverse(operation[1], operation[2])
		} else if command == "rotate" {
			dir := operation[1]
			if unscramble && dir == "right" {
				dir = "left"
			} else if unscramble {
				dir = "right"
			}
			this.rotate(dir, operation[2], unscramble)
		}
	}
}

func (this *Scramble) getScramble() string {
	this.scramble("abcdefgh", false)
	return string(this.charList)
}
func (this *Scramble) getUnscramble() string {
	this.scramble("fbgdceah", true)
	return string(this.charList)
}

func main() {
	scramble := &Scramble{
		UseTest: false,
	}
	scramble.getInput()
	fmt.Println("Day 21 part 1:", scramble.getScramble())
	fmt.Println("Day 21 part 2:", scramble.getUnscramble())
}
