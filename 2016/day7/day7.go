package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Internet struct {
	UseTest   bool
	supernet  [][]string
	hypernet  [][]string
	validIPs  int
	validSSLs int
}

func getSSLPattern(text string, set map[string]bool) map[string]bool {
	if len(text) < 2 {
		return set
	}
	prev := text[0]
	for i := 0; i < len(text)-1; i++ {
		if prev == text[i] {
			continue
		}
		if prev == text[i+1] {
			set[text[i-1:i+2]] = true
		}
		prev = text[i]
	}
	return set
}

func hasABBA(text string) bool {
	if len(text) < 3 {
		return false
	}
	prev := text[0]
	for i := 1; i < len(text)-2; i++ {
		if prev == text[i] {
			continue
		}
		if prev == text[i+2] && text[i] == text[i+1] {
			return true
		}
		prev = text[i]
	}
	return false
}

func (this *Internet) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}

	file, _ := os.Open(inputFile)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.FieldsFunc(line, func(r rune) bool {
			return r == '[' || r == ']'
		})
		nonBrackets := make([]string, 0)
		brackets := make([]string, 0)
		for i, str := range splitted {
			if i%2 == 0 {
				nonBrackets = append(nonBrackets, str)
			} else {
				brackets = append(brackets, str)
			}
		}
		this.supernet = append(this.supernet, nonBrackets)
		this.hypernet = append(this.hypernet, brackets)
	}
	defer file.Close()
}

func (this *Internet) checkIPs() {
	length := len(this.supernet)

	for i := 0; i < length; i++ {

		nonBracketTLS := false
		BracketTLS := false
		ABAset := make(map[string]bool)
		BABset := make(map[string]bool)

		for _, str := range this.supernet[i] {
			if hasABBA(str) {
				nonBracketTLS = true
			}
			ABAset = getSSLPattern(str, ABAset)
		}

		for _, str := range this.hypernet[i] {
			BABset = getSSLPattern(str, BABset)
			if hasABBA(str) {
				BracketTLS = true
			}
		}

		for ABA, _ := range ABAset {
			BAB := string(ABA[1]) + string(ABA[0]) + string(ABA[1])
			_, exists := BABset[BAB]
			if exists {
				this.validSSLs++
				break
			}
		}

		if nonBracketTLS && !BracketTLS {
			this.validIPs++
		}
	}
}

func (this *Internet) getValidIPs() int {
	return this.validIPs
}

func (this *Internet) getValidSSL() int {
	return this.validSSLs
}

func main() {
	internet := &Internet{
		UseTest: false,
	}
	internet.getInput()
	internet.checkIPs()
	fmt.Println("Day 7 part 1:", internet.getValidIPs())
	fmt.Println("Day 7 part 2:", internet.getValidSSL())
}
