import collections

numbers = []
with open("input-test.txt") as f:
    numbers = sorted(list(map(int, f.readlines())))
    numbers = [0] + numbers + [max(numbers)+3]

def differences(numbers):
    return [b-a for a,b in zip(numbers, numbers[1:])]

def noofarr(base, numbers):
    if len(numbers) == 0:
        return 0
    elif len(numbers) == 1:
        return 1
    else:
        res = 0
        for i in [1, 2, 3]:
            try:
                next = numbers.index(numbers[0] + i, 1)
                res += noofarr(base[:] + [numbers[0]], numbers[next:])
            except:
                1
        return res

def noofarr_partitions(numbers):
    diffs = list(map((lambda x: x[1]-x[0]), list(zip(numbers, numbers[1:]))))
    next3 = 0
    result = 1
    while len(numbers) > 0 and len(diffs) > 0:
        next3 = diffs.index(3)
        upperlimit = next3+2
        lowerlimit = next3+1
        result *= noofarr([], numbers[:upperlimit])
        numbers = numbers[lowerlimit:]
        diffs = diffs[lowerlimit:]
    return result

diffdict = collections.Counter(differences(numbers))
print("(part 1) prod =", diffdict[1]*diffdict[3])

print("(part 2) number of arrangements = ", noofarr_partitions(numbers))
