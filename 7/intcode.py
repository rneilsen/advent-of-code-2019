# an Intcode computer built according to specifications on Advent of Code 2019

class Intcode:
	"""A computer running an Intcode program"""

	def __init__(self, inputprogram):
		self.prog = list(inputprogram)
		self.pos = 0
		self.rel_base = 0
	
	def run(self, inputvalue=None):
		"""Run the computer with a given input value, until reaching 
		the next halting instruction. Returns all outputs generated,
		in order, as a list. 99 opcode appends None to list before ending"""
		inputused = False
		outputs = []

		while True:
			instr = self.prog[self.pos]
			verb = instr % 100

			if verb == 1:
				# OPCODE 01: ADD (3 params)
				# take params 1,2 and store sum at pointer param 3
				params = self.getparams(2)
				self.write(self.read(self.pos+3), params[1] + params[2])
				self.step(4)
			elif verb == 2:
				# OPCODE 02: MULTIPLY (3 params)
				# takes params 1,2 and store product at pointer param 3
				params = self.getparams(2)
				self.write(self.read(self.pos+3), params[1] * params[2])
				self.step(4)
			elif verb == 3:
				# OPCODE 03: STORE INPUT (1 param, halting)
				# store the input at pointer param 1
				if inputvalue is None:
					raise Exception("Intcode program expected input, was given None")
				elif inputused:
					return outputs
				else:
					self.write(self.read(self.pos+1), inputvalue)
					inputused = True
					self.step(2)
			elif verb == 4:
				# OPCODE 04: SEND OUTPUT (1 param)
				# take pointer param 1 and append to output
				params = self.getparams(1)
				outputs.append(params[1])
				self.step(2)
			elif verb == 5:
				# OPCODE 05: JUMP IF TRUE (2 params)
				# if param 1 is nonzero, set pos to value from second param
				params = self.getparams(2)
				if params[1] != 0:
					self.goto(params[2])
				else:
					self.step(3)
			elif verb == 6:
				# OPCODE 06: JUMP IF FALSE (2 params)
				# if param 1 is zero, set pos to value from second param
				params = self.getparams(2)
				if params[1] == 0:
					self.goto(params[2])
				else:
					self.step(3)
			elif verb == 7:
				# OPCODE 07: LESS THAN (3 params)
				# if param 1 < param 2, store 1 (else 0) in pointer param 3
				params = self.getparams(2)
				if params[1] < params[2]:
					self.write(self.read(self.pos+3), 1)
				else:
					self.write(self.read(self.pos+3), 0)
				self.step(4)
			elif verb == 8:
				# OPCODE 08: EQUALS (3 params)
				# if param 1 == param 2, store 1 (else 0) in pointer param 3
				params = self.getparams(2)
				if params[1] == params[2]:
					self.write(self.read(self.pos+3), 1)
				else:
					self.write(self.read(self.pos+3), 0)
				self.step(4)
			elif verb == 9:
				# OPCODE 09: ADD TO RELATIVE BASE (1 param)
				# take param 1 and add to the current relative base
				params = self.getparams(1)
				self.rel_base += params[1]
				self.step(2)
			elif verb == 99:
				# OPCODE 99: TERMINATE (halting)
				outputs.append(None)
				return outputs
			else:
				# Unknown opcode
				raise Exception(f"Unknown Opcode: {verb}, at pos {self.pos}")
		
	def write(self, write_pos, val):
		if write_pos > len(self.prog):
			self.prog += [0 for i in range(write_pos - len(self.prog) + 2)]
		self.prog[write_pos] = val
	
	def read(self, read_pos):
		if read_pos > len(self.prog):
			self.prog += [0 for i in range(read_pos - len(self.prog) + 2)]
		return(self.prog[read_pos])
	
	def goto(self, goto_pos):
		if goto_pos > len(self.prog):
			self.prog += [0 for i in range(goto_pos - len(self.prog) + 2)]
		self.pos = goto_pos
	
	def step(self, step_num):
		self.goto(self.pos + step_num)

	def getmode(self, instr, n):
		return (instr // 10**(n+2)) % 10

	def getparams(self, num):
		# pulls 'num' value/pointers from the program starting at position pos
		# params[0] will always be the instruction
		instr = self.prog[self.pos]
		params = [instr % 100]
		for i in range(num):
			mode = self.getmode(instr,i)
			if mode == 0:
				# mode 0: position mode
				params.append(self.read(self.read(self.pos + i + 1)))
			elif mode == 1:
				# mode 1: immediate mode
				params.append(self.read(self.pos + i + 1))
			elif mode == 2:
				# mode 2: relative mode
				params.append(self.read(self.read(self.pos + i + 1) + self.rel_base))
			else:
				raise Exception(f"Unknown mode: {mode} in instruction {instr} at pos {pos}")
		return params

def parse_program(instring):
	return [int(x) for x in instring.strip().split(",")]