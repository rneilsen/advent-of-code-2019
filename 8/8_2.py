WIDTH = 25
HEIGHT = 6

infile = "input.txt"

f = open(infile)
raw_input = f.read().strip()
f.close()

if len(raw_input) % (WIDTH*HEIGHT) != 0:
	raise Exception(f"Error: {infile} does not contain a multiple of {WIDTH}x{HEIGHT} digits.")

raw_input = list(map(int,list(raw_input)))

rows = [raw_input[i:i+WIDTH] for i in range(0,len(raw_input),WIDTH)]
layers = [rows[i:i+HEIGHT] for i in range(0, len(rows), HEIGHT)]

num_layers = len(layers)

display = [[-1 for i in range(WIDTH)] for j in range(HEIGHT)]

for i in range(HEIGHT):
	for j in range(WIDTH):
		layer_number = 0
		while layers[layer_number][i][j] == 2:
			layer_number += 1
		display[i][j] = layers[layer_number][i][j]

render = {0: ' ', 1: '%'}
output = [[render[d] for d in display[i]] for i in range(HEIGHT)]

for row in output:
	print(''.join(row))