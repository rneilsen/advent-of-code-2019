infile = "input.txt"

f = open(infile)
prog = list(map(int, str(f.read()).split(',')))

prog[1] = 12
prog[2] = 2

pos = 0

# opcode reader
while prog[pos] != 99:
	if prog[pos] == 1:
		prog[prog[pos + 3]] = prog[prog[pos + 1]] + prog[prog[pos + 2]]
	elif prog[pos] == 2:
		prog[prog[pos + 3]] = prog[prog[pos + 1]] * prog[prog[pos + 2]]
	else:
		print(f"ERROR: pos = {pos}\nprog = {prog}\nprog[pos] = {prog[pos]}")
		break
	pos += 4

print(prog[0])