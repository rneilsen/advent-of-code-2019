infile = "/home/richard/python/advent-of-code/6/input.txt"

f = open(infile)
orbitmap = f.read().strip().split()

orbits = {"COM": 0} # dict containing how many objects each key orbits (dir&indir)

for o in orbitmap:
	(centre, orbiter) = o.split(')')
	if centre in orbits:
		orbits[orbiter] = 1 + orbits[centre]
	else:
		orbitmap.append(o)

print(sum(orbits.values()))