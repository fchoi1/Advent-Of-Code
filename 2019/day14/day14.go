package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Stoichiometry struct {
	UseTest    bool
	productMap map[string]Formula
	oreCount   int
}

type Formula struct {
	product   string
	quantity  int
	reactants []Chemical
}

type Chemical struct {
	quantity int
	name     string
}

func ceilDivision(dividend, divisor int) int {
	return int(math.Ceil(float64(dividend) / float64(divisor)))
}

func mapToString(m map[string]int) string {
	var keys []string
	for key := range m {
		keys = append(keys, key)
	}
	sort.Strings(keys)

	var keyValueStrings []string
	for _, key := range keys {
		keyValueStrings = append(keyValueStrings, key+":"+strconv.Itoa(m[key]))
	}

	return strings.Join(keyValueStrings, ",")
}

func (this *Stoichiometry) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.productMap = make(map[string]Formula)
	for scanner.Scan() {
		line := scanner.Text()
		formula := strings.Split(line, " => ")
		reactants := strings.FieldsFunc(formula[0], func(r rune) bool { return r == ' ' || r == ',' })
		products := strings.Fields(formula[1])
		chemicalList := []Chemical{}
		for i := 0; i < len(reactants); i += 2 {
			quantity, _ := strconv.Atoi(reactants[i])
			chemicalList = append(chemicalList, Chemical{quantity, reactants[i+1]})
		}
		productQuantity, _ := strconv.Atoi(products[0])
		this.productMap[products[1]] = Formula{products[1], productQuantity, chemicalList}

	}
	defer file.Close()
}

func (this *Stoichiometry) countOres(target string, targetQuantity int, extra map[string]int) int {
	oreCount := 0
	if target == "ORE" {
		return targetQuantity
	}

	formula := this.productMap[target]
	formulaQuantity := ceilDivision(targetQuantity, formula.quantity)

	for _, chem := range formula.reactants {
		remain := chem.quantity * formulaQuantity
		count, exist := extra[chem.name]
		if exist {
			if remain < count {
				extra[chem.name] -= remain
				continue
			}
			delete(extra, chem.name)
			remain -= count
			if remain == 0 {
				continue
			}
		}
		oreCount += this.countOres(chem.name, remain, extra)
	}
	_, extraExists := extra[target]
	if extraExists {
		extra[target] += (formula.quantity * formulaQuantity) - targetQuantity
	} else if (formula.quantity*formulaQuantity)-targetQuantity != 0 {
		extra[target] = (formula.quantity * formulaQuantity) - targetQuantity
	}
	return oreCount
}

func (this *Stoichiometry) countFuel() int {
	extra := make(map[string]int)
	this.oreCount = this.countOres("FUEL", 1, extra)
	return this.oreCount
}

func (this *Stoichiometry) getMaxFuel() int {
	max := 1_000_000_000_000
	min := 1_000_000_000_000 / this.oreCount
	var mid int
	extra := make(map[string]int)
	for max > min {
		mid = (max + min + 1) / 2
		count := this.countOres("FUEL", mid, extra)
		if count > 1_000_000_000_000 {
			max = mid - 1
		} else {
			min = mid
		}
	}
	return max
}

func main() {
	stoichiometry := &Stoichiometry{
		UseTest: false,
	}
	stoichiometry.getInput()
	fmt.Println("Day 14 part 1:", stoichiometry.countFuel())
	fmt.Println("Day 14 part 2:", stoichiometry.getMaxFuel())
}
