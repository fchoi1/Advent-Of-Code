package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
	"strconv"
	"strings"
)

type Shuffler struct {
	UseTest  bool
	commands [][]string
}

func (this *Shuffler) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.commands = [][]string{}

	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Fields(line)
		this.commands = append(this.commands, splitted[len(splitted)-2:])
	}

	defer file.Close()
}

// MATH! https://codeforces.com/blog/entry/72593
func (this *Shuffler) shuffle(card int, length int, loop int) (int, int) {
	a := 1
	b := 0
	var c, d int

	for _, command := range this.commands {
		cmd := command[0]
		a %= length
		b %= length
		switch cmd {
		case "new":
			c = -1
			d = -1
		case "cut":
			val, _ := strconv.Atoi(command[1])
			c = 1
			d = -val

		case "increment":
			val, _ := strconv.Atoi(command[1])
			c = val
			d = 0
		}
		a *= c
		b = b*c + d
	}

	// Big int Constants
	len_big := big.NewInt(int64(length))
	len_big_2 := new(big.Int).Sub(len_big, big.NewInt(2))
	loop_big := big.NewInt(int64(loop))
	a_big_2 := big.NewInt((1 - int64(a)))
	a_big := big.NewInt((int64(a)))
	b_big := big.NewInt((int64(b)))
	start_big := big.NewInt(int64(card))

	I_big := new(big.Int).Exp(a_big_2, len_big_2, len_big)
	// Ax + B
	A_big := new(big.Int).Exp(a_big, loop_big, len_big)
	B_big := new(big.Int)
	B_big.Mul(new(big.Int).Mul(new(big.Int).Sub(big.NewInt(1), A_big), I_big), b_big)
	B_big.Mod(B_big, len_big)

	// Calculate position given card
	pos_big := new(big.Int).Mul(A_big, start_big)
	pos_big.Add(pos_big, B_big)
	pos_big.Mod(pos_big, len_big)

	// Reverse for card instead
	inverse_big := new(big.Int).Exp(A_big, len_big_2, len_big)
	card_big := new(big.Int).Sub(start_big, B_big)
	card_big.Mul(card_big, inverse_big)
	card_big.Mod(card_big, len_big)

	return int(pos_big.Int64()), int(card_big.Int64())
}

func (this *Shuffler) getCard(isPart2 bool) int {
	card := 2019
	length := 10007
	loop := 1
	if isPart2 {
		card = 2020
		length = 119_315_717_514_047
		loop = 101_741_582_076_661
		_, cardVal := this.shuffle(card, length, loop)
		return cardVal
	}
	if this.UseTest{}

	position, _ := this.shuffle(card, length, loop)
	return position
}

func main() {
	shuffler := &Shuffler{
		UseTest: true,
	}
	shuffler.getInput()
	fmt.Println("Day 22 part 1:", shuffler.getCard(false))
	fmt.Println("Day 22 part 2:", shuffler.getCard(true))
}
