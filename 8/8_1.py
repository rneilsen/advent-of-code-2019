WIDTH = 25
HEIGHT = 6

infile = "input.txt"

f = open(infile)
raw_input = f.read().strip()
f.close()

if len(raw_input) % (WIDTH*HEIGHT) != 0:
	raise Exception(f"Error: {infile} does not contain a multiple of {WIDTH}x{HEIGHT} digits.")

rows = [raw_input[i:i+WIDTH] for i in range(0,len(raw_input),WIDTH)]
layers = [rows[i:i+HEIGHT] for i in range(0, len(rows), HEIGHT)]

num_layers = len(layers)

digit_counts = [dict([(str(i),0) for i in range(10)]) for l in layers]
# a list with one dict per layer, each dict containing the number of each digit
# in the corresponding layer

# count each digit in each layer
for i in range(num_layers):
	for j in range(HEIGHT):
		for k in range(WIDTH):
			digit_counts[i][layers[i][j][k]] += 1

min_0s_found = WIDTH*HEIGHT + 1
min_0s_layer = -1

for i in range(num_layers):
	if digit_counts[i]['0'] < min_0s_found:
		min_0s_found = digit_counts[i]['0']
		min_0s_layer = i

print(digit_counts[min_0s_layer]['1'] * digit_counts[min_0s_layer]['2'])