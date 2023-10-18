package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"os"
)

type Vault struct {
	UseTest  bool
	Hash     string
	shortest Path
	longest  Path
}

type Path struct {
	x, y   int
	dirStr string
	steps  int
}

func (this *Vault) getInput() {
	inputFile := "input.txt"
	if this.UseTest {
		inputFile = "input-test.txt"
	}
	file, _ := os.Open(inputFile)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		this.Hash = scanner.Text()
	}
	defer file.Close()
}

func hashMD5(input string) string {
	hash := md5.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

func inBounds(x int, y int) bool {
	return x >= 0 && x < 4 && y >= 0 && y < 4
}

func (this *Vault) getPaths() {
	queue := []Path{{0, 0, "", 0}}
	dirMap := [4][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
	dirList := []string{"U", "D", "L", "R"}
	for len(queue) > 0 {
		path := queue[0]
		queue = queue[1:]
		if path.x == 3 && path.y == 3 {
			this.longest = path
			if this.shortest == (Path{}) {
				this.shortest = path
			}
			continue
		}
		hashed := hashMD5(this.Hash + path.dirStr)
		for i, char := range hashed[:4] {
			if char >= 'b' && char <= 'f' {
				dx, dy := dirMap[i][0], dirMap[i][1]
				if inBounds(dx+path.x, dy+path.y) {
					newPath := Path{
						x:      dx + path.x,
						y:      dy + path.y,
						dirStr: path.dirStr + dirList[i],
						steps:  path.steps + 1,
					}
					queue = append(queue, newPath)
				}
			}
		}

	}
}
func (this *Vault) getShortest() string {
	return this.shortest.dirStr
}

func (this *Vault) getLongest() int {
	return this.longest.steps
}

func main() {
	vault := &Vault{
		UseTest: false,
	}
	vault.getInput()
	vault.getPaths()
	fmt.Println("Day 17 part 1:", vault.getShortest())
	fmt.Println("Day 17 part 2:", vault.getLongest())
}
