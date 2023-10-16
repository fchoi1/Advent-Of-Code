package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"os"
	"strconv"
)

type Pad struct {
	UseTest bool
	Salt    string
}

func hashMD5(input string) string {
	hash := md5.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

func (this *Pad) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.Salt = scanner.Text()
	}
	defer file.Close()
}

func (this *Pad) getIndex() int {
	num := 0
	keyList := [][]string{}
	targetKey = 64
	var hashStr string
	for len(this.Password) < 8 || !isArrayFull(password2Arr) {
		hashStr = this.Salt + strconv.Itoa(num)
		hashed = hashMD5(hashStr)
		fmt.Println(hashed)
		num++
	}

	return 0
}

func main() {
	pad := &Pad{
		UseTest: false,
	}
	pad.getInput()
	fmt.Println("Day 14 part 1:", pad.getIndex())
	// fmt.Println("Day 14 part 2:", pad.getMaxLocations())
}
