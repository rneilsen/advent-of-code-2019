from intcode import Intcode
import itertools

# INFILE = "/home/richard/python/advent-of-code/7/simple4.txt"
# INFILE = "/home/richard/python/advent-of-code/7/simple5.txt"
INFILE = "/home/richard/python/advent-of-code/7/input.txt"


f = open(INFILE)
prog = [int(x) for x in f.read().strip().split(",")]
f.close()

maxvalue = -1

for PHASES in itertools.permutations(range(5,10)):
	amps = [Intcode(prog) for n in range(5)]

	# initialise all amps by giving their phase as input
	for amp,ph in zip(amps,PHASES):
		amp.run(ph)

	value = 0 # initial input to amp A

	# run all amps in cycle until amps all halted (returns None)
	while amps != []:
		amp = amps.pop(0)
		values = amp.run(value)
		value = values[0]
		if values[-1] != None:
			amps.append(amp)
	
	if value > maxvalue:
		maxvalue = value
	
print(maxvalue)
