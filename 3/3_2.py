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

# nodes example: (2,3) -> [1,0,4]
# indicates node (2,3) was visited 
# with length 1 by wire 0, not visited by wire 1, length 4 by wire 2
nodes = {}

for n in range(len(inlists)):
	# iterate through the lists in inlists
	# for each list update nodes with the first visit to each from this wire
	curpos = (0,0)
	length = 0

	# iterate through instructions in inlists[n] and update nodes[n]
	for inst in inlists[n]:
		numsteps = int(inst[1:])
		dir = directions[inst[0]]

		for i in range(numsteps):
			curpos = vadd(curpos, dir)
			length += 1

			if curpos not in nodes:
				# this node has not been visited by any wire yet
				nodes[curpos] = [0 for i in range(len(inlists))]
				nodes[curpos][n] = length
			elif nodes[curpos][n] == 0:
				# this node has been visited, but not by this wire
				nodes[curpos][n] = length
			else:
				# this node has been visited, by this wire
				pass

# find signal delays to nodes visited by every wire
delays = []
for node in nodes:
	if 0 not in nodes[node]:
		delays.append(sum(nodes[node]))

print(min(delays))
