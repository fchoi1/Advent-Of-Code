package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"math"
	"os"
	"reflect"
	"sort"
	"strconv"
	"strings"
)

type Pad struct {
	UseTest bool
	Salt    string
}

func hashMD5(input string) string {
	hash := md5.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}
func removeIndexes(slice interface{}, indexes []int) interface{} {
	v := reflect.ValueOf(slice)
	if v.Kind() != reflect.Slice {
		return nil
	}
	indexSet := make(map[int]bool)
	for _, idx := range indexes {
		indexSet[idx] = true
	}
	result := reflect.MakeSlice(v.Type(), 0, 0)
	for i := 0; i < v.Len(); i++ {
		if !indexSet[i] {
			result = reflect.Append(result, v.Index(i))
		}
	}
	return result.Interface()
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

func (this *Pad) getIndex(isPart2 bool) int {
	foundIndex := math.MaxInt64
	keyIndex := []int{}
	charList := []string{}
	keyList := []int{}
	var char2Add string
	for num := 0; num < foundIndex; num++ {
		has3 := false
		for len(keyIndex) > 0 && num-keyIndex[0] > 1000 {
			keyIndex = keyIndex[1:]
			charList = charList[1:]
		}
		hashed := hashMD5(this.Salt + strconv.Itoa(num))
		if isPart2 {
			for i := 0; i < 2016; i++ {
				hashed = hashMD5(hashed)
			}
		}
		indexToRemove := []int{}
		for i, char := range hashed {
			if i+2 < 32 && hashed[i:i+3] == strings.Repeat(string(char), 3) && !has3 {
				char2Add = string(char)
				has3 = true
			}
			if i+4 < 32 && hashed[i:i+5] == strings.Repeat(string(char), 5) {
				for i, char2Match := range charList {
					if string(char) == char2Match {
						indexToRemove = append(indexToRemove, i)
						keyList = append(keyList, keyIndex[i])
						if len(keyList) == 64 {
							foundIndex = num + 5000
						}
					}
				}
				break // only first instance of 5?
			}
		}
		keyIndex = removeIndexes(keyIndex, indexToRemove).([]int)
		charList = removeIndexes(charList, indexToRemove).([]string)
		if has3 {
			keyIndex = append(keyIndex, num)
			charList = append(charList, char2Add)
		}
	}
	sort.Ints(keyList)
	return keyList[63]
}

func main() {
	pad := &Pad{
		UseTest: false,
	}
	pad.getInput()
	fmt.Println("Day 14 part 1:", pad.getIndex(false))
	fmt.Println("Day 14 part 2:", pad.getIndex(true))
	//Total Runtime ~ 8.8s
}
