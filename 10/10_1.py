from math import gcd

examples = {"simple1.txt": (3, 4, 8),
            "simple2.txt": (5, 8, 33),
            "simple3.txt": (1, 2, 35),
            "simple4.txt": (6, 3, 41),
            "simple5.txt": (11, 12, 210)}

infile = "input.txt"


def vadd(v1, v2):
    return((v1[0] + v2[0], v1[1] + v2[1]))


raw_rows = []
f = open("/home/richard/python/advent-of-code/10/" + infile)
for r in f:
    raw_rows.append(list(r.strip()))
f.close()

height = len(raw_rows)
width = len(raw_rows[0])

asteroids = set()
for i in range(width):
    for j in range(height):
        if raw_rows[j][i] == "#":
            asteroids.add((i,j))

most_visible = 0
best_spot = (-1,-1)

for a in asteroids:
    vis_roids = asteroids.copy()
    vis_roids.remove(a)
    for b in asteroids:
        if a != b:    
            diff = (b[0] - a[0], b[1] - a[1])
            g = gcd(diff[0], diff[1])
            diff = (diff[0] / g, diff[1] / g)
            blocked = vadd(diff, b)
            while 0 <= blocked[0] <= width + 1 and 0 <= blocked[1] <= height + 1:
                vis_roids.discard(blocked)
                blocked = vadd(diff, blocked)
    if len(vis_roids) > most_visible:
        best_spot = a
        most_visible = len(vis_roids)

print(best_spot, ":", most_visible)