package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Room struct {
	ID       int
	Checksum string
	Words    []string
	Message  string
}

type Security struct {
	UseTest          bool
	Rooms            []Room
	sumRooms         int
	NorthPoleStorage int
}

type Pair struct {
	Key   string
	Value int
}

func sortMap(charMap map[string]int) []Pair {
	pairs := make([]Pair, 0, len(charMap))
	for key, value := range charMap {
		pairs = append(pairs, Pair{key, value})
	}

	sort.Slice(pairs, func(i, j int) bool {
		if pairs[i].Value == pairs[j].Value {
			return pairs[i].Key < pairs[j].Key
		}
		return pairs[i].Value > pairs[j].Value
	})
	return pairs
}

func (this *Security) getInput() {
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
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == '[' || r == ']' || r == ' ' || r == '-'
		})

		words := splitted[:len(splitted)-2]
		id, _ := strconv.Atoi(splitted[len(splitted)-2])
		checkSum := splitted[len(splitted)-1]

		room := Room{
			ID:       id,
			Checksum: checkSum,
			Words:    words,
		}
		this.Rooms = append(this.Rooms, room)
	}
	defer file.Close()
}

func (this *Security) checkRoom() {
	sum := 0
	filteredRooms := []Room{}

	for _, room := range this.Rooms {
		charMap := make(map[string]int)
		for _, word := range room.Words {
			for _, char := range word {
				charStr := string(char)
				if _, exists := charMap[charStr]; exists {
					charMap[charStr] += 1
				} else {
					charMap[charStr] = 1
				}
			}
		}
		pairs := sortMap(charMap)
		occurrence := ""
		for i, pair := range pairs {
			if i >= 5 {
				break
			}
			occurrence += pair.Key
		}
		if occurrence == room.Checksum {
			sum += room.ID
			filteredRooms = append(filteredRooms, room)
		}
	}
	this.sumRooms = sum
	this.Rooms = filteredRooms
}

func (this *Security) decryptRoom() {
	for _, room := range this.Rooms {
		room.Message = ""
		shift := room.ID % 26
		for _, word := range room.Words {
			shiftedWord := ""
			for _, char := range word {
				asciiValue := int(char)
				shiftedAscii := (asciiValue-'a'+shift)%26 + 'a'
				shiftedWord += string(shiftedAscii)
			}
			room.Message += shiftedWord + " "
		}

		if strings.Contains(room.Message, "northpole") {
			this.NorthPoleStorage = room.ID
			return
		}
	}
}

func (this *Security) getSumRooms() int {
	return this.sumRooms
}

func (this *Security) getNorthPoleRoom() int {
	return this.NorthPoleStorage
}

func main() {
	security := &Security{
		UseTest: false,
	}
	security.getInput()
	security.checkRoom()
	security.decryptRoom()
	fmt.Println("Day 4 part 1:", security.getSumRooms())
	fmt.Println("Day 4 part 2:", security.getNorthPoleRoom())
}
