# an Intcode computer built according to specifications on Advent of Code 2019


class Intcode:
    """A computer running an Intcode program"""

    def __init__(self, inputprogram):
        self.prog = list(inputprogram)
        self.pos = 0
        self.rel_base = 0

    def run(self, inputs=None):
        """Run the program with the given inputs (as a list, in order).
        Will halt and return all generated outputs as a list when it reaches
        a halting opcode like 3 or 99. On reaching a 99, it adds None
        to the output list before returning it."""

        if type(inputs) is not list and inputs is not None:
            raise Exception(f"Inputs must be a list; was given {inputs}")

        outputs = []

        while True:
            instr = self.prog[self.pos]
            opcode = instr % 100

            if opcode == 1:
                # Opcode 1: Add and store (3 params)
                pointers = self.get_param_pointers(self.pos,
                                                   [True, True, False])

                value = (self.read_at_position(pointers[0])
                         + self.read_at_position(pointers[1]))
                self.write_at_position(pointers[2], value)

                self.pos += 4
            elif opcode == 2:
                # Opcode 2: Multiply and store (3 params)
                pointers = self.get_param_pointers(self.pos,
                                                   [True, True, False])

                value = (self.read_at_position(pointers[0])
                         * self.read_at_position(pointers[1]))
                self.write_at_position(pointers[2], value)

                self.pos += 4
            elif opcode == 3:
                # Opcode 3: Store input (1 param)
                if inputs is None:
                    raise Exception("Program expected inputs, was given None")
                if inputs == []:    # run out of provided inputs
                    return outputs
                pointers = self.get_param_pointers(self.pos, [False])
                value = inputs.pop(0)
                self.write_at_position(pointers[0], value)

                self.pos += 2
            elif opcode == 4:
                # Opcode 4: Output (1 param)
                pointers = self.get_param_pointers(self.pos, [True])
                outputs.append(self.read_at_position(pointers[0]))

                self.pos += 2
            elif opcode == 5:
                # Opcode 5: Jump if true, i.e. nonzero (2 params)
                pointers = self.get_param_pointers(self.pos,
                                                   [True, True])
                if self.read_at_position(pointers[0]) != 0:
                    self.pos = self.read_at_position(pointers[1])
                else:
                    self.pos += 3
            elif opcode == 6:
                # Opcode 6: Jump if false, i.e. zero (2 params)
                pointers = self.get_param_pointers(self.pos,
                                                   [True, True])
                if self.read_at_position(pointers[0]) == 0:
                    self.pos = self.read_at_position(pointers[1])
                else:
                    self.pos += 3
            elif opcode == 7:
                # Opcode 7: Less than (3 params)
                pointers = self.get_param_pointers(self.pos,
                                                   [True, True, False])
                values = [self.read_at_position(pointers[0]),
                          self.read_at_position(pointers[1])]
                values.append(1 if values[0] < values[1] else 0)
                self.write_at_position(pointers[2], values[2])

                self.pos += 4
            elif opcode == 8:
                # Opcode 8: Equal to (3 params)
                pointers = self.get_param_pointers(self.pos,
                                                   [True, True, False])
                values = [self.read_at_position(pointers[0]),
                          self.read_at_position(pointers[1])]
                values.append(1 if values[0] == values[1] else 0)
                self.write_at_position(pointers[2], values[2])

                self.pos += 4
            elif opcode == 9:
                # Opcode 9: Add to relative base (1 params)
                pointers = self.get_param_pointers(self.pos, [True])
                self.rel_base += self.read_at_position(pointers[0])

                self.pos += 2
            elif opcode == 99:
                # Opcode 99: Terminate
                outputs.append(None)
                return outputs
            else:
                raise Exception(f"Unknown opcode: {opcode} in instr {instr}"
                                + f" at position {self.pos}")

    def get_param_pointers(self, pos, modes_allow_imm):
        """Takes a position of an instruction and a list of Boolean values
        representing whether immediate mode is allowed for each param in turn,
        and returns a list of "cleaned" pointers (accounting for modes in the
        instruction) pointing at the correct positions for the original functio
        to find all its relevant parameters"""
        num_params = len(modes_allow_imm)
        instr = self.prog[self.pos]
        modes = self.get_modes(instr, num_params)
        pointers = []

        for i in range(num_params):
            pointers.append(self.fix_pointer(
                self.pos + i + 1, modes[i], modes_allow_imm[i]))
        return pointers

    def get_modes(self, instr, n):
        return [instr // (10**(i+2)) % 10 for i in range(n)]

    def read_at_position(self, pos):
        if pos > len(self.prog):
            self.prog += [0 for i in range(len(self.prog), pos + 1)]
        return self.prog[pos]

    def write_at_position(self, pos, value):
        if pos >= len(self.prog):
            self.prog += [0 for i in range(len(self.prog), pos + 1)]
        self.prog[pos] = value

    def fix_pointer(self, pointer, mode, allow_immediate=True):
        if not allow_immediate and mode == 1:
            raise Exception("This pointer cannot be in immediate mode.")
        if mode == 0:
            # position mode: give the address at the address we were given
            return self.read_at_position(pointer)
        elif mode == 1:
            # immediate mode: give back the given address
            return pointer
        elif mode == 2:
            # relative mode: give address at given address, plus rel_base
            return self.read_at_position(pointer) + self.rel_base
        else:
            raise Exception(f"Unknown mode: {mode}")


def parse_program(instring):
    return [int(x) for x in instring.strip().split(",")]


def readfile(filepath):
    f = open(filepath)
    s = f.read().strip()
    f.close()
    return s