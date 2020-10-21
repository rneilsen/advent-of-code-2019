infile = "/home/richard/python/advent-of-code/3/input.txt"
directions = {"L": (-1,0), "U": (0,1), "R": (1,0), "D": (0,-1)}

def vadd(a,b):
	# return to vector sum of a and b
	if len(a) != 2:
		raise Exception("Not a length 2 vector: a = {a}")
	elif len(a) != 2:
		raise Exception("Not a length 2 vector: b = {b}")
	else:
		return (a[0] + b[0], a[1] + b[1])

f = open(infile)

# read input file and split into the two wire instruction lists
inlists = [s.split(",") for s in f.read().split("\n")[:-1]]

# print(f"inlists[1] = {inlists[1]}, inlists[2] = {inlists[2]}")

wires = []
for n in range(len(inlists)):
	# iterate through the lists in inlists and create a positions list
	# for each wire in wires[n]
	wires.append(set())
	curpos = (0,0)

	# iterate through instructions in inlists[n] and insert positions into wires[n]
	for inst in inlists[n]:
		num = int(inst[1:])
		dir = directions[inst[0]]

		for i in range(num):
			curpos = vadd(curpos, dir)
			wires[n].add(curpos)

# for n in range(len(inlists)):
# 	print(f"{inlists[n]} --> {wires[n]}")

crossings = wires[0].intersection(wires[1])
print(sorted([abs(cross[0]) + abs(cross[1]) for cross in crossings])[0])
