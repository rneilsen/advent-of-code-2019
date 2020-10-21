ORIGIN = "YOU"
DEST = "SAN"

infile = "simple2.txt"
f = open(infile)
orbitmap = f.read().strip().split()
f.close()

# build dict of orbiters with their respective centres
orbits = {"COM": ""}
for o in orbitmap:
	(centre, orbiter) = o.split(')')
	orbits[orbiter] = centre


current_node = ORIGIN
chain_from_origin = [current_node]
while current_node != "COM":
	current_node = orbits[current_node]
	chain_from_origin.append(current_node)

current_node = DEST
chain_from_dest = [current_node]
while current_node != "COM":
	current_node = orbits[current_node]
	chain_from_dest.append(current_node)

for node in chain_from_dest:
	if node in chain_from_origin:
		print(chain_from_dest.index(node) + chain_from_origin.index(node) - 2)
		break
	
