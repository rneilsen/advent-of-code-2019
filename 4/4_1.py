LOWBOUND = 145852
HIGHBOUND = 616942

def isvalid(n):
	containsdouble = False
	l = [int(c) for c in str(n)]
	for i in range(len(l) - 1):
		if l[i] > l[i+1]:
			return False
		elif l[i] == l[i+1]:
			containsdouble = True
	# non-decreasing is satisfied, now True/False is equiv to containsdouble
	return containsdouble		

print(f"111111: {isvalid(111111)}")
print(f"223450: {isvalid(223450)}")
print(f"123789: {isvalid(123789)}")

validcount = 0
for n in range(LOWBOUND, HIGHBOUND):
	if isvalid(n):
		validcount += 1

print(validcount)