from math import gcd, atan2, sqrt, pi

IMS = (26, 29)   # calculated in 10_1.py

examples = {"simple1.txt": (3, 4, 8),
            "simple2.txt": (5, 8, 33),
            "simple3.txt": (1, 2, 35),
            "simple4.txt": (6, 3, 41),
            "simple5.txt": (11, 12, 210)}

infile = "input.txt"


# def vadd(v1, v2):
#     return((v1[0] + v2[0], v1[1] + v2[1]))
def dist(v1, v2):
    return sqrt((v2[0] - v1[0])**2 + (v2[1] - v1[1])**2)


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
        elif raw_rows[j][i] == "X":
            IMS = (i,j)

angles = {}

# construct angles database
for a in asteroids:
    if a == IMS:
        continue
    angle = atan2(a[0] - IMS[0] , IMS[1] - a[1])     # this seems to be right
    if angle < 0: 
        angle += 2*pi

    if angle not in angles:
        angles[angle] = [a]
    else:
        # insert asteroid a into angles[angle] reverse-sorted by distance
        d1 = dist(a, IMS)
        inserted = False
        for i in range(len(angles[angle])):
            if d1 > dist(IMS, angles[angle][i]):
                angles[angle].insert(i, a)
                inserted = True
                break
        if not inserted:
            angles[angle].append(a)

# delete asteroids cycling angles until 200 deleted
print(len(angles), "asteroids, IMS =", IMS)

anglelist = sorted(list(angles))
for a in anglelist:
    x = str(round(a,3))
    print (x + "00"[:5 - len(x)], ":", angles[a])

numdeleted = 0
i = 0

while numdeleted <= len(asteroids):
    angle = anglelist[i]

    if angles[angle] != []:
        cur = angles[angle].pop()
        numdeleted += 1
        if numdeleted == 200:
            print(f"Deletion {numdeleted}: {cur}")

    if i >= len(angles) - 1:
        i = 0
    else:
        i += 1
        
