package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Factory struct {
	UseTest    bool
	Factory    string
	compareBot int
	targetHigh int
	targetLow  int
	targetBot  int
	Bots       map[int]*FactoryBot
	Outputs    map[int]*Output
	Values     map[int]*FactoryBot
}

type FactoryBot struct {
	id      int
	lowVal  int
	highVal int
	low     interface{}
	high    interface{}
}

type Output struct {
	id     int
	values []int
}

func (f *Factory) getOrCreateOutput(id int) *Output {
	output, exists := f.Outputs[id]
	if !exists {
		output = &Output{
			id:     id,
			values: []int{},
		}
		f.Outputs[id] = output
	}
	return output
}

func (f *Factory) getOrCreateBot(id int) *FactoryBot {
	bot, exists := f.Bots[id]
	if !exists {
		bot = &FactoryBot{
			id:   id,
			low:  nil,
			high: nil,
		}
		f.Bots[id] = bot
	}
	return bot
}

func (this *Factory) updateBots(bot *FactoryBot, value int) {

	if bot.lowVal == 0 {
		bot.lowVal = value
	} else if value > bot.lowVal {
		bot.highVal = value
	} else {
		bot.highVal, bot.lowVal = bot.lowVal, value
	}

	if bot.highVal != 0 && bot.lowVal != 0 {
		if bot.highVal == this.targetHigh && bot.lowVal == this.targetLow {
			this.targetBot = bot.id
		}
		if lowBot, isFactoryBot := bot.low.(*FactoryBot); isFactoryBot {
			this.updateBots(lowBot, bot.lowVal)
		} else if output, isOutput := bot.low.(*Output); isOutput {
			output.values = append(output.values, bot.lowVal)
		}
		if highBot, isFactoryBot := bot.high.(*FactoryBot); isFactoryBot {
			this.updateBots(highBot, bot.highVal)
		} else if output, isOutput := bot.low.(*Output); isOutput {
			output.values = append(output.values, bot.highVal)
		}
		bot.highVal, bot.lowVal = 0, 0
	}
}

func (this *Factory) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)

	var value int
	var botNum int
	this.Bots = make(map[int]*FactoryBot)
	this.Values = make(map[int]*FactoryBot)
	this.Outputs = make(map[int]*Output)
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Fields(line)

		if splitted[0] == "value" {
			value, _ = strconv.Atoi(splitted[1])
			botNum, _ = strconv.Atoi(splitted[5])

			Bot := this.getOrCreateBot(botNum)
			this.Values[value] = Bot
		} else {
			botNum, _ := strconv.Atoi(splitted[1])
			botLow, _ := strconv.Atoi(splitted[6])
			botHigh, _ := strconv.Atoi(splitted[11])
			isOutput1 := splitted[5] == "output"
			isOutput2 := splitted[10] == "output"

			Bot := this.getOrCreateBot(botNum)
			var newLow, newHigh interface{}
			if isOutput1 {
				newLow = this.getOrCreateOutput(botLow)
			} else {
				newLow = this.getOrCreateBot(botLow)
			}
			if isOutput2 {
				newHigh = this.getOrCreateOutput(botHigh)
			} else {
				newHigh = this.getOrCreateBot(botHigh)
			}
			Bot.low = newLow
			Bot.high = newHigh
		}
	}
	defer file.Close()
}

func (this *Factory) sortBots() {
	if this.UseTest {
		this.targetLow = 2
		this.targetHigh = 3
	} else {
		this.targetLow = 17
		this.targetHigh = 61
	}
	for value, bot := range this.Values {
		this.updateBots(bot, value)
	}
}

func (this *Factory) getBot() int {
	return this.targetBot
}

func (this *Factory) getProduct() int {
	out0, ok0 := this.Outputs[0]
	out1, ok1 := this.Outputs[1]
	out2, ok2 := this.Outputs[2]
	if !ok0 || len(out0.values) == 0 || !ok1 || len(out1.values) == 0 || !ok2 || len(out2.values) == 0 {
		return 0
	}
	return out0.values[0] * out1.values[0] * out2.values[0]
}

func main() {
	factory := &Factory{
		UseTest: false,
	}
	factory.getInput()
	factory.sortBots()
	fmt.Println("Day 10 part 1:", factory.getBot())
	fmt.Println("Day 10 part 2:", factory.getProduct())
}
