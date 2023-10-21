package main

import (
	"bufio"
	"fmt"
	"os"
	"reflect"
	"sort"
	"strconv"
	"strings"
)

type Storage struct {
	UseTest  bool
	NodeMap  map[string]Node
	adjMap   map[string][]Node
	NodeList []Node
	zeroNode Node
	goalNode Node
	height   int
	width    int
}
type Node struct {
	size    int
	used    int
	avail   int
	percent int
	x       int
	y       int
	key     string
}

func (this *Storage) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	this.NodeMap = make(map[string]Node)
	this.NodeList = []Node{}
	for scanner.Scan() {
		line := scanner.Text()
		splitted := strings.Fields(line)
		node := strings.FieldsFunc(splitted[0], func(r rune) bool {
			return r == '-' || r == '/'
		})
		if node[0] != "dev" {
			continue
		}
		size, _ := strconv.Atoi(splitted[1][:len(splitted[1])-1])
		used, _ := strconv.Atoi(splitted[2][:len(splitted[2])-1])
		avail, _ := strconv.Atoi(splitted[3][:len(splitted[3])-1])
		percent, _ := strconv.Atoi(splitted[4][:len(splitted[4])-1])
		x, _ := strconv.Atoi(node[3][1:])
		y, _ := strconv.Atoi(node[4][1:])
		key := strconv.Itoa(x) + "," + strconv.Itoa(y)
		newNode := Node{size, used, avail, percent, x, y, key}
		if used == 0 {
			this.zeroNode = newNode
		}
		if y == 0 {
			this.goalNode = newNode
		}
		this.NodeMap[key] = newNode
		this.width, this.height = x+1, y+1
		this.NodeList = append(this.NodeList, newNode)
	}
	defer file.Close()
}

func sortNodes(nodeList []Node, key string) {
	sort.Slice(nodeList, func(i, j int) bool {
		nodeValue1 := reflect.ValueOf(nodeList[i])
		nodeValue2 := reflect.ValueOf(nodeList[j])
		field1 := nodeValue1.FieldByName(key)
		field2 := nodeValue2.FieldByName(key)
		if field1.IsValid() && field2.IsValid() && field1.Type() == field2.Type() {
			switch field1.Kind() {
			case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
				return field1.Int() > field2.Int()
			}
		}
		return false
	})
}

func copyPath(original []Node) []Node {
	copiedSlice := make([]Node, len(original))
	copy(copiedSlice, original)
	return copiedSlice
}

func (this *Storage) getPairs() int {
	N := len(this.NodeList)
	usedList := make([]Node, N)
	availList := make([]Node, N)
	copy(usedList, this.NodeList)
	copy(availList, this.NodeList)
	sortNodes(usedList, "used")
	sortNodes(availList, "avail")
	seen := make(map[string]bool)
	usedIndex, availIndex, pairs := 0, 0, 0

	for usedIndex < N-1 && availIndex < N-1 {
		currUsed, currAvail := usedList[usedIndex], availList[availIndex]
		usedSize, availSize := currUsed.used, currAvail.avail
		if usedSize != 0 && usedSize <= availSize {
			pairs += N - usedIndex - 1 // Only 1 zero node exists
			if seen[currUsed.key] {
				pairs-- // subtract duplicate
			}
		}
		for availSize > usedSize {
			availIndex++
			currAvail = availList[availIndex]
			availSize = currAvail.avail
			seen[currAvail.key] = true
		}
		usedIndex++
	}
	return pairs
}

func (this *Storage) generateAdjacencyMap() {
	this.adjMap = make(map[string][]Node)
	dirMap := [][]int{{0, -1}, {0, 1}, {1, 0}, {-1, 0}}
	for _, node := range this.NodeList {
		for _, dir := range dirMap {
			newX, newY := dir[0]+node.x, dir[1]+node.y
			if newX >= 0 && newX < this.width && newY >= 0 && newY < this.height {
				key := strconv.Itoa(newX) + "," + strconv.Itoa(newY)
				newNode := this.NodeMap[key]
				if node.used <= newNode.size {
					this.adjMap[node.key] = append(this.adjMap[node.key], newNode)
				}
			}
		}
	}
}

func (this *Storage) bfs(start Node, end Node, visited map[string]bool) int {
	// visited has the current goal node inside
	steps := 0
	queue := []Node{start}
	for len(queue) > 0 {
		temp := []Node{}
		for _, curr := range queue {
			fmt.Println(curr.key)
			if curr == end {
				return steps
			}
			for _, node := range this.adjMap[curr.key] {
				if visited[node.key] {
					continue
				}
				visited[node.key] = true
				temp = append(temp, node)
			}
		}
		steps++
		queue = temp
	}
	fmt.Println("not found in bfs")
	return -1
}

// func (this *Storage) findGoalPaths() [][]Node { // ??? on straight line???
// 	visited := make(map[string]bool)
// 	visited[this.goalNode.key] = true
// 	paths := [][]Node{}
// 	var findPath func(node Node, path []Node, visited map[string]bool)
// 	findPath = func(currNode Node, path []Node, visited map[string]bool) {
// 		if currNode.key == "0,0" {
// 			paths = append(paths, copyPath(path))
// 			return
// 		}

// 		_, exists := this.adjMap[currNode.key]
// 		if !exists {
// 			return
// 		}
// 		visited[currNode.key] = true
// 		for _, node := range this.adjMap[currNode.key] {
// 			if visited[node.key] {
// 				continue
// 			}
// 			if node.x > currNode.x {
// 				// fmt.Println("why go right?")
// 			}
// 			// Backtrack
// 			path = append(path, node)
// 			// visited[currNode.key] = true

// 			findPath(node, path, visited)
// 			// visited[node.key] = false
// 			path = path[:len(path)-1]
// 		}
// 		visited[currNode.key] = false

// 	}
// 	findPath(this.goalNode, []Node{this.goalNode}, visited)
// 	return paths
// }

func printPath(paths [][]Node) {

	for i, path := range paths {
		coords := []string{}
		fmt.Println("path #", i)
		for _, node := range path {
			coords = append(coords, node.key)
		}
		fmt.Println(coords)
	}
}
func (this *Storage) getLeastSteps() int {

	this.generateAdjacencyMap()

	currNode := this.goalNode
	path := []Node{}
	for currNode != this.NodeMap["0,0"] {
		fmt.Println("curr", currNode.key)
		path = append(path, currNode)
		for _, node := range this.adjMap[currNode.key] {
			if node.x < currNode.x {
				currNode = node
				break
			}
		}
	}

	fmt.Println("path", len(path), path)

	//bfs
	// key position of goal and empty disk
	// exit when 0,0 is empty and goal is beside exit

	// check if goal size fits in size of neighburs

	// first check various paths of Goal to destination
	// need like  a couple , dont think we need to backtrac???

	maxSize := this.zeroNode.avail
	goalSize := this.goalNode.used
	fmt.Println("sizes", maxSize, goalSize)
	// fmt.Println("shortest", this.bfs(this.NodeMap["0,0"], this.goalNode, make(map[string]bool)))
	fmt.Println("shortest", this.bfs(this.zeroNode, this.goalNode, make(map[string]bool)))

	// paths := this.findGoalPaths()
	// fmt.Println("num pahts", len(paths))
	// printPath(paths)

	// for i, path := range paths {
	// 	fmt.Println("path #", i)
	// 	for _, node := range path {
	// 		fmt.Println(node.key)

	// 	}
	// }

	// make map to exclude any data that can't be transferred
	return 1
}

func main() {
	storage := &Storage{
		UseTest: false,
	}
	storage.getInput()
	fmt.Println("Day 22 part 1:", storage.getPairs())
	fmt.Println("Day 22 part 2:", storage.getLeastSteps())
}
