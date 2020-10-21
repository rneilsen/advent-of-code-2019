import intcode2

infile = "input.txt"

prog = intcode2.parse_program(intcode2.readfile(infile))

m = intcode2.Intcode(prog)

print(m.run([1]))