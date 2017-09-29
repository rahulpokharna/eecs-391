import fileinput
lst = []
for line in fileinput.input('test.txt'):
    lst.append(line)
for x in range(len(lst)):
    print(lst[len(lst) - x - 1], end='')
    