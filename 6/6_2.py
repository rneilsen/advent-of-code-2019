infile = "input.txt"
f = open(infile)
orbitmap = f.read().strip().split()
f.close()

def get_indirect_orbiters(orbits,centre):
	direct_orbiters = orbits[centre]
	indirect_orbiters = set()
	for orbiter in direct_orbiters:
		indirect_orbiters += orbits[orbiter]
		indirect_orbiters += get_indirect_orbiters(orbits,orbiter)

orbits = {"COM": set()} # dict containing the list of DIRECT orbiters

for o in orbitmap:
	(centre, orbiter) = o.split(')')
	if centre not in orbits:
		orbits[centre] = set(orbiter)
	else:
		orbits[centre].add(orbiter)
	if orbiter not in orbits:
		orbits[orbiter] = set()


	
print(orbits)