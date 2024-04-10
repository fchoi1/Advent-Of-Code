package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Computer struct {
	intCode      []int
	receive      []int
	relativeBase int
	index        int
	id           int
}
type Network struct {
	UseTest   bool
	IntCode   []int
	computers []*Computer
	firstY    int
	NATy      int
	NATx      int
}

func (this *Network) getInput() {
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
		for i := 0; i < 10_000; i++ {
			this.IntCode = append(this.IntCode, 0)
		}
	}
	defer file.Close()
}
func (this *Network) parseOpCode(n int) (int, []int) {
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

func (this *Network) runProgram(index int, relativeBase int, intCode []int, input []int) ([]int, int) {
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
			a = intCode[a+relativeBase]
		}

		switch code {
		case 3, 4:
			if code == 3 {
				if len(input) == 0 {
					return output, index
				}
				if params[0] == 2 {
					intCode[intCode[index+1]+relativeBase] = input[0]
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
			relativeBase += a
			index += 2
			continue
		}

		if params[1] == 0 {
			b = intCode[b]
		} else if params[1] == 2 {
			b = intCode[b+relativeBase]
		}

		if params[2] == 2 {
			c += relativeBase
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

func (this *Network) allDone() bool {
	for _, computer := range this.computers {
		if len(computer.receive) > 0 {
			return false
		}
	}
	return true
}

func (this *Network) runNetwork() {
	// Make computers
	for i := 0; i < 50; i++ {
		intCodeCopy := make([]int, len(this.IntCode))
		copy(intCodeCopy, this.IntCode)
		newComp := Computer{intCodeCopy, []int{}, 0, 0, i}
		_, newComp.index = this.runProgram(newComp.index, newComp.relativeBase, newComp.intCode, []int{newComp.id})
		this.computers = append(this.computers, &newComp)
	}
	seen := make(map[int]bool)
	// Run Network
	for {
		for _, computer := range this.computers {
			var output []int
			if len(computer.receive) == 0 {
				computer.receive = []int{-1}
			}

			output, computer.index = this.runProgram(computer.index, computer.relativeBase, computer.intCode, computer.receive)
			for i := 0; i < len(output); i += 3 {
				target := output[i]
				X := output[i+1]
				Y := output[i+2]
				if target == 255 {
					if this.firstY == 0 {
						this.firstY = Y
					}
					this.NATx, this.NATy = X, Y
				} else {
					this.computers[target].receive = append(this.computers[target].receive, X, Y)
				}
			}
			// Reset Recieved
			computer.receive = []int{}
		}
		if this.allDone() {
			if _, ok := seen[this.NATy]; ok {
				break
			}
			seen[this.NATy] = true
			this.computers[0].receive = []int{this.NATx, this.NATy}
		}
	}
}

func (this *Network) getPacket() int {
	return this.firstY
}
func (this *Network) getNATy() int {
	return this.NATy
}

func main() {
	network := &Network{
		UseTest: false,
		IntCode: []int{},
	}
	network.getInput()
	network.runNetwork()
	fmt.Println("Day 23 part 1:", network.getPacket())
	fmt.Println("Day 23 part 2:", network.getNATy())
}
