package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type File struct {
	UseTest     bool
	file        string
	compressed  string
	compressed2 string
}

func parseMarker(text string) (int, int) {
	splitted := strings.FieldsFunc(text, func(r rune) bool {
		return r == '(' || r == 'x'
	})
	num1, _ := strconv.Atoi(splitted[0])
	num2, _ := strconv.Atoi(splitted[1])
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
func getCompressedLength(text string, times int) int {

	var str string
	markerFound := false
	var markStart int
	var skipIndex int
	length := 0
	for i, char := range text {
		if i < skipIndex {
			continue
		}
		if !markerFound && char == '(' {
			markerFound = true
			markStart = i
		} else if !markerFound {
			str += string(char)
			length++
		}
		if markerFound && char == ')' {
			markerFound = false
			strLen, times := parseMarker(text[markStart:i])
			skipIndex = i + strLen + 1
			length += getCompressedLength(text[i+1:skipIndex], times)
		}
	}
	return length * times
}

func (this *File) compressFile() {
	markerFound := false
	var markStart int
	var skipIndex int
	for i, char := range this.file {

		if i < skipIndex {
			continue
		}
		if !markerFound && char == '(' {
			markerFound = true
			markStart = i
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
	this.compressFile()
	return len(this.compressed)
}

func (this *File) getFileLength2() int {
	return getCompressedLength(this.file, 1)
}

func main() {
	file := &File{
		UseTest: false,
	}
	file.getInput()
	fmt.Println("Day 9 part 1:", file.getFileLength())
	fmt.Println("Day 9 part 2:", file.getFileLength2())
}
