package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type File struct {
	UseTest    bool
	file       string
	compressed string
}

func parseMarker(text string) (int, int) {
	splitted := strings.FieldsFunc(text, func(r rune) bool {
		return r == '(' || r == 'x'
	})
	num1, _ := strconv.Atoi(splitted[0])
	num2, _ := strconv.Atoi(splitted[1])
	fmt.Println(text)

	return num1, num2
}

func (this *File) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.file += string(line)
	}
	defer file.Close()
}

func (this *File) compressFile() {
	markerFound := false
	var markStart int
	var skipIndex int
	for i, char := range this.file {

		if i < skipIndex{
			fmt.Println("skip", i, string(char))
			continue
		}

		if !markerFound && char == '(' {
			markerFound = true
			markStart = i
			fmt.Println("found marker", i)
		} else if !markerFound {
			this.compressed += string(char)
		}
		if markerFound && char == ')' {
			markerFound = false
			strLen, times := parseMarker(this.file[markStart:i])
			skipIndex = i + strLen + 1
			repeated := strings.Repeat(this.file[i+1:skipIndex], times)
			this.compressed += repeated
		}
	}
}

func (this *File) getFileLength() int {
	return len(this.compressed)
}

func main() {

	file := &File{
		UseTest: false,
	}
	file.getInput()
	file.compressFile()
	fmt.Println("Day 8 part 1:", file.getFileLength())
	fmt.Println("Day 8 part 2:")
}
