from intcode2 import readfile, parse_program, Intcode

prog = Intcode(parse_program(readfile("input.txt")))

SPRITES = {0: "   ", 1: "+++", 2: "[%]", 3: "---", 4: "(O)"}

output = prog.run()
objects = [output[i:i+3] for i in range(0, len(output) - 1, 3)]

width = max([obj[0] for obj in objects])
height = max([obj[1] for obj in objects])

screen = [[" " for x in range(width + 1)] for y in range(height + 1)]

num_blocks = 0
for obj in objects:
    (x, y) = (obj[0], obj[1])
    screen[y][x] = SPRITES[obj[2]]
    if obj[2] == 2:
        num_blocks += 1

print(f"Number of block tiles: {num_blocks}")