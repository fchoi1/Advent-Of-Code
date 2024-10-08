from typing import List, Optional


class Calories:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            data = []
            for line in file1:
                coords = line.strip().split(" -> ")
                x1, y1 = coords[0].split(",")
                x2, y2 = coords[1].split(",")
                data.append([(int(x1), int(y1)), (int(x2), int(y2))])
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.input = self.getInput()

    def countOverlap(self, isPart2: bool = False) -> int:
        count = 0
        points = {}
        overlap = set()
        for p1, p2 in self.input:
            if p1[0] == p2[0]:
                for i in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                    points[(p1[0], i)] = points.get((p1[0], i), 0) + 1
                    if points[(p1[0], i)] == 2:
                        overlap.add((p1[0], i))
                        count += 1
            elif p1[1] == p2[1]:
                for i in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
                    points[(i, p1[1])] = points.get((i, p1[1]), 0) + 1
                    if points[(i, p1[1])] == 2:
                        overlap.add((i, p1[1]))
                        count += 1
            elif isPart2:
                # print()
                start, end = p1, p2
                if p1[0] > p2[0]:
                    start, end = p2, p1
                while start != end:
                    # print("runing", start, end)
                    points[start] = points.get(start, 0) + 1
                    if points[start] == 2:
                        overlap.add(start)
                        count += 1
                    if end[1] > start[1]:
                        start = (start[0] + 1, start[1] + 1)
                    else:
                        start = (start[0] + 1, start[1] - 1)
                points[start] = points.get(start, 0) + 1
                if points[start] == 2:
                        overlap.add(start)
                        count += 1
            else:
                print("wrong", p1,p2)
        print(len(overlap))
        return count


if __name__ == "__main__":
    calories = Calories(False)
    # print("Day 1 part 1:", calories.countOverlap())
    print("Day 1 part 2:", calories.countOverlap(True))
