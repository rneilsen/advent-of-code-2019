from itertools import permutations
from numpy import sign

INFILE = "/home/richard/python/advent-of-code/12/input.txt"
NUMSTEPS = 1000

class Moon:
    """A moon object with a position and a velocity"""

    def __init__(self, position):
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.pos_z = position[2]
        self.vel_x = self.vel_y = self.vel_z = 0
    
    def __repr__(self):
        return(
            f"pos=<x={str(self.pos_x).rjust(3)}, "
            + f"y={str(self.pos_y).rjust(3)}, "
            + f"z={str(self.pos_z).rjust(3)}>, "
            + f"vel=<x={str(self.vel_x).rjust(3)}, "
            + f", y={str(self.vel_y).rjust(3)}, "
            + f", z={str(self.vel_z).rjust(3)}>")
    
    def potential_energy(self):
        return(abs(self.pos_x) + abs(self.pos_y) + abs(self.pos_z))

    def kinetic_energy(self):
        return(abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z))
        
# create moons list from INFILE
moons = []
with open(INFILE) as f:
    for row in f:
        x = int(row[row.find('x=')+2:row.find(', y')])
        y = int(row[row.find('y=')+2:row.find(', z')])
        z = int(row[row.find('z=')+2:row.find('>')])
        moons.append(Moon((x, y, z)))

for n in range(NUMSTEPS):
    # calculate velocity changes from all pairs of moons
    for (m1, m2) in permutations(moons, 2):
        m1.vel_x += sign(m2.pos_x - m1.pos_x)
        m1.vel_y += sign(m2.pos_y - m1.pos_y)
        m1.vel_z += sign(m2.pos_z - m1.pos_z)
    
    # apply velocities to all moons
    for m in moons:
        m.pos_x += m.vel_x
        m.pos_y += m.vel_y
        m.pos_z += m.vel_z

# calculate total energy in system
energy_total = 0
for m in moons:
    energy_total += m.kinetic_energy() * m.potential_energy()
print(f"Total energy = {energy_total}")

