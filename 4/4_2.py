LOWBOUND = 145852
HIGHBOUND = 616942

def isvalid(n):
	containsdouble = False
	l = [int(c) for c in str(n)]
	for i in range(len(l) - 1):
		if l[i] > l[i+1]:
			return False
		elif l[i] == l[i+1]:
			if 0 < i < len(l) - 2:
				# in middle
				if l[i-1] != l[i] and l[i+1] != l[i+2]:
					containsdouble = True
			elif i == 0:
				if l[i+1] != l[i+2]:
					containsdouble = True
			elif i == len(l) - 2:
				if l[i-1] != l[i]:
					containsdouble = True
			else:
				raise Exception("Error: invalid i")
	# non-decreasing is satisfied, now True/False is equiv to containsdouble
	return containsdouble		

print(f"112233: {isvalid(112233)}")
print(f"123444: {isvalid(123444)}")
print(f"111122: {isvalid(111122)}")

validcount = 0
for n in range(LOWBOUND, HIGHBOUND):
	if isvalid(n):
		validcount += 1

print(validcount)