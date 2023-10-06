package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Door struct {
	UseTest   bool
	Password  string
	Password2 string
	Id        string
}

func hashMD5(input string) string {
	hash := md5.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

func isArrayFull(arr []string) bool {
	for _, value := range arr {
		if value == "" {
			return false
		}
	}
	return true
}

func (this *Door) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, err := os.Open(inputFile)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		this.Id = line
	}
	defer file.Close()
}

func (this *Door) getPassword(isPart2 bool) string {
	if isPart2 {
		return this.Password2
	}
	return this.Password
}

func (this *Door) checkPassword() {
	password2Arr := make([]string, 8)
	num := 0
	hashed := ""
	hashStr := ""
	for len(this.Password) < 8 || !isArrayFull(password2Arr) {
		subset := ""
		for subset != "00000" && num < 100_000_000 {
			hashStr = this.Id + strconv.Itoa(num)
			hashed = hashMD5(hashStr)
			subset = hashed[:5]
			num++
		}
		if len(this.Password) < 8 {
			this.Password += hashed[5:6]
		}
		if !isArrayFull(password2Arr) {
			index, err := strconv.Atoi(hashed[5:6])
			if err != nil {
				continue
			}
			if index >= 0 && index < len(password2Arr) && password2Arr[index] == "" {
				password2Arr[index] = hashed[6:7]
			}
		}
	}
	this.Password2 = strings.Join(password2Arr, "")
}

func main() {
	door := &Door{
		UseTest: false,
	}
	door.getInput()
	door.checkPassword()
	fmt.Println("Day 5 part 1:", door.getPassword(false))
	fmt.Println("Day 5 part 2:", door.getPassword(true))
	// Total Runtime ~4.9s
}
