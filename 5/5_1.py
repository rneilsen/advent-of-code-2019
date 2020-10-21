infile = "/home/richard/python/advent-of-code/5/input.txt"
input_data = -18

def getmode(instr, n):
	return (instr // 10**(n+2)) % 10

def getparams(prog, pos, num):
	# pulls 'num' value/pointers from the program starting at position pos
	# values[0] will always be the instruction
	instr = prog[pos]
	values = [instr % 100]
	for i in range(num):
		mode = getmode(instr,i)
		if mode == 0:
			values.append(prog[prog[pos+i+1]])
		elif mode == 1:
			values.append(prog[pos + 1 + i])
		else:
			raise Exception(f"Unknown parameter: {param} in instruction {instr} at pos {pos}")
	return values

def runopcode(prog):
	pos = 0

	while (prog[pos] % 100) != 99:
		instr = prog[pos]
		verb = instr % 100
		
		if verb == 1:
			# OPCODE 01: ADD (3 params)
			# takes value/pointers in params 1,2 and stores their sum at pointer param 3 
			values = getparams(prog, pos, 3)
			prog[prog[pos+3]] = values[1] + values[2]
			pos += 4
		elif verb == 2:
			# OPCODE 02: MULTIPLY (3 params)
			# takes value/pointers in params 1,2 and stores their product at pointer param 3
			values = getparams(prog, pos, 3)
			prog[prog[pos+3]] = values[1] * values[2]
			pos += 4
		elif verb == 3:
			# OPCODE 03: WRITE INPUT (1 param)
			# takes input and saves in pointer at param 1
			prog[prog[pos+1]] = input_data
			pos += 2
		elif verb == 4:
			# OPCODE 04: READ AND OUTPUT (1 param)
			# takes pointer at param 1 and feeds to output (currently print)
			values = getparams(prog,pos,1)
			print("Output:", values[1])
			pos += 2
		elif verb == 5:
			# OPCODE 05: JUMP IF TRUE (2 params)
			# if param 1 is nonzero, set pos to value from second param
			values = getparams(prog,pos,2)
			if values[1] != 0:
				pos = values[2]
			else:
				pos += 3
		elif verb == 6:
			# OPCODE 06: JUMP IF FALSE (2 params)
			# if param 1 is zero, set pos to value from second param
			values = getparams(prog,pos,2)
			if values[1] == 0:
				pos = values[2]
			else:
				pos += 3
		elif verb == 7:
			# OPCODE 07: LESS THAN (3 params)
			# if param 1 is less than param 2, store 1 (else 0) in pointer param 3
			values = getparams(prog,pos,3)
			if values[1] < values[2]:
				prog[prog[pos+3]] = 1
			else:
				prog[prog[pos+3]] = 0
			pos += 4
		elif verb == 8:
			# OPCODE 08: EQUALS (3 params)
			# if param 1 is equal to param 2, store 1 (else 0) in pointer param 3
			values = getparams(prog,pos,3)
			if values[1] == values[2]:
				prog[prog[pos+3]] = 1
			else:
				prog[prog[pos+3]] = 0
			pos += 4
		else:
			# Unknown opcode
			print(f"ERROR: pos = {pos}\nprog = {prog}\nverb = {verb}")
			break

f = open(infile)
prog = list(map(int, str(f.read()).split(',')))

input_data = 5

runopcode(prog)

# print(prog)
	