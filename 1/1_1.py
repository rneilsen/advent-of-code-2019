infile = "input.txt"

sum = 0
f = open(infile)
for m in f:
	sum += int(m) // 3 - 2

print(sum)