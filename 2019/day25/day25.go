package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Cryostasis struct {
	UseTest      bool
	IntCode      []int
	grid         [][]int
	relativeBase int
}

func getAscii(str string) []int {
	asciiValues := []int{}
	for _, char := range str {
		asciiValues = append(asciiValues, int(char))
	}
	return asciiValues
}

func getString(asciiValues []int) string {
	result := ""
	for _, ascii := range asciiValues {
		result += string(ascii)
	}
	return result
}

func getCmbinations(vals []string) [][]string {
	var result [][]string
	var dfs func(int, []string)

	dfs = func(start int, path []string) {
		if len(path) > 0 {
			temp := make([]string, len(path))
			copy(temp, path)
			result = append(result, temp)
		}
		for i := start; i < len(vals); i++ {
			path = append(path, vals[i])
			dfs(i+1, path)
			path = path[:len(path)-1]
		}
	}
	dfs(0, []string{})
	return result
}

func (this *Cryostasis) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.IntCode = []int{}

	for scanner.Scan() {
		line := scanner.Text()
		strNum := strings.Split(line, ",")
		for _, n := range strNum {
			num, _ := strconv.Atoi(n)
			this.IntCode = append(this.IntCode, num)
		}
		// additional space needed
		for i := 0; i < 250; i++ {
			this.IntCode = append(this.IntCode, 0)
		}
	}
	defer file.Close()
}
func (this *Cryostasis) parseOpCode(n int) (int, []int) {
	code := n % 100
	rest := strconv.Itoa(n / 100)
	arr := []int{}
	for i := len(rest) - 1; i >= 0; i-- {
		intValue, _ := strconv.Atoi(string(rest[i]))
		arr = append(arr, intValue)
	}
	for len(arr) < 3 {
		arr = append(arr, 0)
	}
	return code, arr
}

func (this *Cryostasis) runProgram(index int, intCode []int, input []int) ([]int, int) {
	output := []int{}
	for index < len(intCode) {
		code, params := this.parseOpCode(intCode[index])
		if code == 99 {
			return output, -1
		}

		a, b, c := intCode[index+1], intCode[index+2], intCode[index+3]

		if params[0] == 0 {
			a = intCode[a]
		} else if params[0] == 2 {
			a = intCode[a+this.relativeBase]
		}

		switch code {
		case 3, 4:
			if code == 3 {
				if len(input) == 0 {
					return output, index
				}
				if params[0] == 2 {
					intCode[intCode[index+1]+this.relativeBase] = input[0]
				} else {
					intCode[intCode[index+1]] = input[0]
				}
				input = input[1:]
			} else if code == 4 {
				output = append(output, a)
			}
			index += 2
			continue
		case 9:
			this.relativeBase += a
			index += 2
			continue
		}

		if params[1] == 0 {
			b = intCode[b]
		} else if params[1] == 2 {
			b = intCode[b+this.relativeBase]
		}

		if params[2] == 2 {
			c += this.relativeBase
		}
		switch code {
		case 1:
			intCode[c] = a + b
		case 2:
			intCode[c] = a * b
		case 5, 6:
			if (code == 5 && a != 0) || (code == 6 && a == 0) {
				index = b
			} else {
				index += 3
			}
			continue
		case 7, 8:
			intCode[c] = 0
			if (code == 7 && a < b) || (code == 8 && a == b) {
				intCode[c] = 1
			} else {
				intCode[c] = 0
			}
		}
		index += 4
	}
	return output, -1
}

func (this *Cryostasis) getItems() int {
	commands := []string{
		"east", "take food ration",
		"east", "take manifold",
		"east", "east", "take jam",
		"west", "north", "north", "take fuel cell",
		"south", "east", "take spool of cat6",
		"west", "south", "west", "west", "south", "take prime number",
		"north", "west", "north", "north", "north", "east", "east", "take loom",
		"west", "west", "south", "west", "take mug",
		"east", "south", "west", "north", "west"}
	var index int
	for _, cmd := range commands {
		_, index = this.runProgram(index, this.IntCode, getAscii(cmd+"\n"))
	}
	return index
}

func (this *Cryostasis) reset(index int, items []string) int {
	for _, item := range items {
		_, index = this.runProgram(index, this.IntCode, getAscii("drop "+item+"\n"))
	}
	return index
}

func (this *Cryostasis) sendDroid() string {
	var output []int
	index := this.getItems()
	items := []string{"food ration", "manifold", "jam", "fuel cell", "spool of cat6", "prime number", "loom", "mug"}
	combos := getCmbinations(items)

	for _, combo := range combos {
		index = this.reset(index, items)
		for _, item := range combo {
			_, index = this.runProgram(index, this.IntCode, getAscii("take "+item+"\n"))
		}
		output, index = this.runProgram(index, this.IntCode, getAscii("north\n"))
		if strings.Contains(getString(output), "You may proceed") {
			re := regexp.MustCompile(`\d+`)
			match := re.FindAllString(getString(output), -1)
			return match[0]
		}
	}
	return ""
}

func main() {
	cryostasis := &Cryostasis{
		UseTest: false,
		IntCode: []int{},
	}
	cryostasis.getInput()
	fmt.Println("Day 25 part 1:", cryostasis.sendDroid())
}
