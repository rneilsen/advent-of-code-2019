infile = "./input.txt"
target = 19690720

# import infile and convert to prog and initprog, lists of integers
f = open(infile)
initprog = list(map(int, f.read().rstrip().split(',')))

def run_intcode(intcode):
	prog = intcode.copy()
	pos = 0
	while prog[pos] != 99:
		if prog[pos] == 1:
			# 1 command: take the next two values, add them into position given by third value
			prog[prog[pos + 3]] = prog[prog[pos + 1]] + prog[prog[pos + 2]]
			pos += 4
		elif prog[pos] == 2:
			# 2 command: take values at next two locations
			prog[prog[pos + 3]] = prog[prog[pos + 1]] * prog[prog[pos + 2]]
			pos += 4
		else:
			print(f"ERROR: x = {x}, y = {y}, prog[{pos}] = {prog[pos]}")
			break
	return(prog)

for x in range(100):
	for y in range(100):
		prog = initprog.copy()
		prog[1] = x
		prog[2] = y
		pos = 0

		# run the Intcode
		out = run_intcode(prog)

		if out[0] == target:
			print(f"x = {x}, y = {y}")
			break
