package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
	"strings"
)

type Dragon struct {
	UseTest bool
	Num     string
}

func (this *Dragon) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.Num = scanner.Text()
	}
	defer file.Close()
}

func reverseAndAdd(original *big.Int, length int) *big.Int {
	numBits := original.BitLen()
	leadingZeros := length - numBits
	newOriginal := new(big.Int)
	newOriginal.Set(original)
	newOriginal = newOriginal.Lsh(newOriginal, 1)
	for i := 0; i < leadingZeros; i++ {
		newOriginal = newOriginal.Lsh(newOriginal, 1)
		newOriginal.SetBit(newOriginal, 0, 0)
	}
	for i := 0; i < numBits; i++ {
		bit := original.Bit(i) ^ 1
		newOriginal = newOriginal.Lsh(newOriginal, 1)
		newOriginal.SetBit(newOriginal, 0, bit)
	}
	return newOriginal
}

func reverse(s string) string {
	rns := []rune(s) // convert to rune
	for i, j := 0, len(rns)-1; i < j; i, j = i+1, j-1 {
		rns[i], rns[j] = rns[j], rns[i]
	}
	for i, char := range rns {
		if char == '0' {
			rns[i] = '1'
			continue
		}
		rns[i] = '0'
	}
	return string(rns)
}

func (this *Dragon) getChecksum(isPart2 bool) string {
	var targetLength int
	if this.UseTest {
		targetLength = 20
	} else {
		targetLength = 272
	}
	if isPart2 {
		targetLength = 35_651_584
	}

	currLength := len(this.Num)
	binStr := this.Num

	binInt := new(big.Int)
	binInt.SetString(binStr, 2)

	fmt.Println("bigInt start", binInt, targetLength)

	for currLength < targetLength {
		binInt = reverseAndAdd(binInt, currLength)
		currLength = currLength*2 + 1
	}

	binInt.SetString(binInt.Text(2)[:targetLength], 2)

	// fmt.Println("checksum    :", binInt.Text(2)[:targetLength])

	length := binInt.BitLen()
	fmt.Println("checksum    :", length)
	var leadingZeros int
	for length%2 == 0 {
		tempBigInt := new(big.Int)

		for i := 0; i < leadingZeros/2; i++ {
			tempBigInt = tempBigInt.Lsh(tempBigInt, 1)
			tempBigInt.SetBit(tempBigInt, 0, 1)
		}

		leadingZeros %= 2
		var bit1 uint
		for i := binInt.BitLen() - 1 + leadingZeros; i >= 0; i -= 2 {
			if leadingZeros%2 == 1 {
				bit1 = 0
				leadingZeros = 0
			} else {
				bit1 = binInt.Bit(i)
			}
			bit2 := binInt.Bit(i - 1)
			tempBigInt = tempBigInt.Lsh(tempBigInt, 1)
			tempBigInt.SetBit(tempBigInt, 0, 1^(bit1^bit2))
		}
		binInt = tempBigInt
		length /= 2
		leadingZeros = length - binInt.BitLen()
	}

	checksum := strings.Repeat("0", leadingZeros)
	checksum += binInt.Text(2)

	fmt.Println("now", checksum)
	// fmt.Println("check sum", checksum)

	return checksum
}

func main() {
	dragon := &Dragon{
		UseTest: false,
	}
	dragon.getInput()
	fmt.Println("Day 16 part 1:", dragon.getChecksum(false))
	fmt.Println("Day 16 part 2:", dragon.getChecksum(true))
}
