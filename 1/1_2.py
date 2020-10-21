infile = "input.txt"

sum = 0
f = open(infile)
for m in f:
	mass = int(m)
	while mass > 0:
		mass = int(mass) // 3 - 2
		sum += (mass if mass > 0 else 0)

print(sum)