from intcode2 import readfile, parse_program, Intcode

def vadd(a,b):
	# return to vector sum of a and b
	if len(a) != 2:
		raise Exception("Not a length 2 vector: a = {a}")
	elif len(a) != 2:
		raise Exception("Not a length 2 vector: b = {b}")
	else:
		return (a[0] + b[0], a[1] + b[1])

brain = Intcode(parse_program(readfile("input.txt")))

cur_pos = (0,0)
cur_dir = (0,1)

painted_panels = set()
white_panels = set()

cont = True

while cont:
    next = brain.run([(1 if cur_pos in white_panels else 0)])
    if next[-1] is None:
        cont = False
        print(f"Terminate command given, next = {next}")
        if len(next) < 2:
            break
    
    # paint current panel
    if next[0] == 1:    # paint white
        white_panels.add(cur_pos)
    elif next[0] == 0:               # paint black
        white_panels.discard(cur_pos)
    else:
        raise Exception(f"Invalid instructions from brain: {next}")
    painted_panels.add(cur_pos)

    # turn and move forward
    if next[1] == 0:    # turn left
        cur_dir = (-cur_dir[1], cur_dir[0])
    elif next[1] == 1:  # turn right
        cur_dir = (cur_dir[1], -cur_dir[0])
    else:
        raise Exception(f"Invalid instructions from brain: {next}")
    cur_pos = vadd(cur_pos, cur_dir)

print(len(painted_panels))    
