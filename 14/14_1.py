from math import ceil

recipes = dict()

# build the recipes database
# {'FUEL': (3, {('A',5), ('B',2), ('C',3)})}
with open("/home/richard/python/advent-of-code/14/example1.txt") as f:
    for line in f:
        (reac_raw, prod_raw) = line.strip().split(" => ")
        (prod_qty, prod) = (int(prod_raw.split(' ')[0]), prod_raw.split(' ')[1])
        reac_raw_list = [a.split(' ') for a in reac_raw.split(', ')]
        reactants = dict()
        for r in reac_raw_list:
            (reac, reac_qty) = (r[1], int(r[0]))
            reactants[reac] = reac_qty
        recipes[prod] = (prod_qty, reactants)

needed = {'FUEL': 1}
have = {}
for prod in recipes.keys():
    have[prod] = 0
ore_reqd = 0
cont = True

# calculate amount of ore needed
while needed:
    (need, need_qty) = needed.popitem()
    while have[need] < need_qty:
        for (reac, reac_qty) in recipes[need][1].items():
            if reac == 'ORE':
                ore_reqd += reac_qty
            else:
                if reac in needed:
                    needed[reac] += reac_qty
                else:
                    needed[reac] = reac_qty
        have[need] += reac_qty
    have[need] -= need_qty

print(ore_reqd)