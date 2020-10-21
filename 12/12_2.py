from itertools import permutations
from numpy import sign, lcm

INFILE = "/home/richard/python/advent-of-code/12/input.txt"

class Moon:
    """A moon object with a position and a velocity"""

    def __init__(self, position):
        self.pos = list(position)
        self.vel = [0, 0, 0]
    
    def __repr__(self):
        return(
            f"pos=<x={str(self.pos[0]).rjust(3)}, "
            + f"y={str(self.pos[1]).rjust(3)}, "
            + f"z={str(self.pos[2]).rjust(3)}>, "
            + f"vel=<x={str(self.vel[0]).rjust(3)}, "
            + f", y={str(self.vel[1]).rjust(3)}, "
            + f", z={str(self.vel[2]).rjust(3)}>")
    
    def short_state(self, axis):
        return((self.pos[axis], self.vel[axis]))
        
# create moons list from INFILE
moons = []
with open(INFILE) as f:
    for row in f:
        x = int(row[row.find('x=')+2:row.find(', y')])
        y = int(row[row.find('y=')+2:row.find(', z')])
        z = int(row[row.find('z=')+2:row.find('>')])
        moons.append(Moon((x, y, z)))

steps_reqd = []
# for each axis, calculate number of steps needed for cycle
for i in range(3):
    states = set(tuple([m.short_state(i) for m in moons]))

    cont = True
    n = 0
    while cont:
        # calculate velocity changes from all pairs of moons
        for (m1, m2) in permutations(moons, 2):
            m1.vel[i] += sign(m2.pos[i] - m1.pos[i])
        
        # apply velocities to all moons
        for m in moons:
            m.pos[i] += m.vel[i]

        # test if a previous state achieved
        state = tuple([m.short_state(i) for m in moons])
        if state in states:
            steps_reqd.append(n)
            cont = False
        else:
            states.add(state)
        
        n += 1

print(lcm.reduce(steps_reqd))