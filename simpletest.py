from intcode2 import readfile, parse_program, Intcode

testfile = "/home/richard/python/advent-of-code/tests/9_test_1.txt"

prog = parse_program(readfile(testfile))

m = Intcode(prog)

print(m.run())
