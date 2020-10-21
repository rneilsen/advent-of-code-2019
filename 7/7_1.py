from intcode import Intcode
import itertools

# INFILE = "/home/richard/python/advent-of-code/7/simple1.txt"
# PHASES = [4,3,2,1,0]
# INFILE = "/home/richard/python/advent-of-code/7/simple2.txt"
# PHASES = [0,1,2,3,4]
# INFILE = "/home/richard/python/advent-of-code/7/simple3.txt"
# PHASES = [1,0,4,3,2]
INFILE = "/home/richard/python/advent-of-code/7/input.txt"

f = open(INFILE)
prog = [int(x) for x in f.read().strip().split(",")]
f.close()

maxvalue = -1

for PHASES in itertools.permutations(range(5)):
	amps = [Intcode(prog) for n in range(5)]

	# initialise all amps by giving their phase as input
	for amp,ph in zip(amps,PHASES):
		amp.run(ph)

	value = 0 # initial input to amp A

	while amps != []:
		amp = amps.pop(0)
		value = amp.run(value)[0]
	if value > maxvalue:
		maxvalue = value
	
print(maxvalue)
