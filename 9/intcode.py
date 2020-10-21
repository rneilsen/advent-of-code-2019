# an Intcode computer built according to specifications on Advent of Code 2019


class Intcode:
    """A computer running an Intcode program"""

    def __init__(self, inputprogram):
        self.prog = list(inputprogram)
        self.pos = 0
        self.rel_base = 0
    
    def run(self, inputvalue=None):
        """Run the computer with a given input value, until reaching 
        the next halting instruction. Returns all outputs generated,
        in order, as a list. 99 opcode appends None to list before ending"""
        inputused = False
        outputs = []

        while True:
            verb = self.read_value(self.pos, 1) % 100
            instr = self.read_value(self.pos, 1)

            if verb == 1:
                # OPCODE 01: ADD (3 params)
                # take params 1,2 and store sum at pointer param 3
                modes = self.get_modes(instr, 3)
                pointers = self.get_value_pointers(self.pos + 1, modes)
                (a, b) = (self.read_value(pointers[0], 1), 
                          self.read_value(pointers[1], 1))
                self.write_value(a+b, pointers[2], modes[2])
                # aaagh how do I get write to work
                self.step(4)
            elif verb == 2:
                # OPCODE 02: MULTIPLY (3 params)
                # takes params 1,2 and store product at pointer param 3
                modes = self.get_modes(instr, 3)
                pointers = self.get_value_pointers(self.pos + 1, modes)
                (a, b) = (self.read_value(pointers[0], 1), 
                          self.read_value(pointers[1], 1))
                self.write(pointers[2], a*b)
                self.step(4)
            elif verb == 3:
                # OPCODE 03: STORE INPUT (1 param, halting)
                # store the input at pointer param 1
                if inputvalue is None:
                    raise Exception("Intcode program expected input, was given"
                                    + " None")
                elif inputused:
                    return outputs
                else:
                    modes = self.get_modes(instr, 1)
                    pointers = self.get_value_pointers(self.pos + 1, modes)
                    self.write(pointers[0], inputvalue)
                    inputused = True
                    self.step(2)
            elif verb == 4:
                # OPCODE 04: SEND OUTPUT (1 param)
                # take pointer param 1 and append to output
                modes = self.get_modes(instr, 1)
                outputs.append(self.get_value(self.pos + 1, modes[0]))
                self.step(2)
            elif verb == 5:
                # OPCODE 05: JUMP IF TRUE (2 params)
                # if param 1 is nonzero, set pos to value from second param
                modes = self.get_modes(instr, 2)
                values = [self.get_value(self.pos + 1, modes[0])]
                if values[0] != 0:
                    self.goto(self.get_pointer(self.pos + 2, modes[1]))
                else:
                    self.step(3)
            elif verb == 6:
                # OPCODE 06: JUMP IF FALSE (2 params)
                # if param 1 is zero, set pos to value from second param
                modes = self.get_modes(instr, 2)
                values = [self.get_value(self.pos + 1, modes[0])]
                if values[0] == 0:
                    self.goto(self.get_pointer(self.pos + 2, modes[1]))
                else:
                    self.step(3)
            elif verb == 7:
                # OPCODE 07: LESS THAN (3 params)
                # if param 1 < param 2, store 1 (else 0) in pointer param 3
                modes = self.get_modes(instr, 3)
                values = [self.get_value(self.pos + i + 1, modes[i]) for i in range(2)]
                dest = self.get_pointer(self.pos+3, modes[2])

                if values[0] < values[1]:
                    self.write(dest, 1)
                else:
                    self.write(dest, 0)
                self.step(4)
            elif verb == 8:
                # OPCODE 08: EQUALS (3 params)
                # if param 1 == param 2, store 1 (else 0) in pointer param 3
                modes = self.get_modes(instr, 3)
                values = [self.get_value(self.pos + i + 1, modes[i]) for i in range(2)]
                dest = self.get_pointer(self.pos+3, modes[2])

                if values[0] == values[1]:
                    self.write(dest, 1)
                else:
                    self.write(dest, 0)
                self.step(4)
            elif verb == 9:
                # OPCODE 09: ADD TO RELATIVE BASE (1 param)
                # take param 1 and add to the current relative base
                modes = self.get_modes(instr, 1)
                values = [self.get_value(self.pos + 1, modes[0])]
                self.rel_base += values[0]
                self.step(2)
            elif verb == 99:
                # OPCODE 99: TERMINATE (halting)
                outputs.append(None)
                return outputs
            else:
                # Unknown opcode
                raise Exception(f"Unknown Opcode: {verb}, at pos {self.pos}")

    def read_value(self, read_pointer, mode):
        # go to a position (read_pointer), read what is there, and return the appropriate value
        if read_pointer < 0:
            raise Exception(f"Asked to read value from invalid pointer {read_pointer}")
        elif read_pointer > len(self.prog):
            self.prog += [0 for i in range(read_pointer - len(self.prog) + 2)]
        
        if mode == 0:
            # position mode: interpret the value at read_pointer as a pointer,
            # and return what is at its dereferenced value 
            return self.read_value(read_pointer, 1)
        elif mode == 1:
            # immediate mode: interpret the value at read_pointer as a value,
            # and return it
            return self.prog[read_pointer]
        elif mode == 2:
            # relative mode: interpret the value at read-pointer as a pointer,
            # add rel_base, and return what is at the dereferenced value
            return self.read_value(read_pointer + self.rel_base, 1)
        else:
            raise Exception(f"read_value given invalid mode {mode}")
    
    def get_value_pointers(self, position, modes):
        # returns a list of pointers, starting at position, interpreting modes
        pointers = []
        pos = position
        for mode in modes:
            if mode == 0:
                # position mode: this is a pointer, give it
                pointers.append(self.read_value(position, 1))
            elif mode == 1:
                # immediate mode: this is a value, give its pointer
                pointers.append(pos)
            elif mode == 2:
                # relative mode: this is a pointer, give (it + rel_base)
                pointers.append(self.read_value(position, 1) + self.rel_base)
            else:
                raise Exception(f"get_value_pointers given invalid mode: {mode}")
        return pointers

    def write_value(self, value, write_pointer, mode):
        if write_pointer < 0:
            raise Exception(f"write_value asked to write invalid position: {write_pointer}")
        elif write_pointer > len(self.prog):
            self.prog += [0 for i in range(write_pointer) - len(self.prog) + 2]
        
        if mode == 0:
            # position mode: write_pointer is a pointer, write value there
            self.prog[write_pointer] = value
        elif mode == 1:
            # immediate mode: invalid for writing
            raise Exception(f"write_value cannot write in immediate mode")
        elif mode == 2:
            # relative mode: write_pointer is a pointer, add rel_base and write theree
            self.write_value(value, write_pointer + self.rel_base, 0)
        else:
            raise Exception(f"write_value given invalid mode: {mode}")

    
    def write(self, write_pos, val):
        if write_pos < 0:
            raise Exception(f"Asked to write invalid position {write_pos}")
        elif write_pos > len(self.prog):
            self.prog += [0 for i in range(write_pos - len(self.prog) + 2)]
        self.prog[write_pos] = val
    
    def get_value(self, read_pos, mode):
        if read_pos < 0:
            raise Exception(f"Asked to get value in invalid position {read_pos}")
        elif mode == 0:
            return self.read(self.read(read_pos))
        elif mode == 1:
            return self.read(read_pos)
        elif mode == 2:
            return self.read(self.read(read_pos) + self.rel_base)
        else:
            raise Exception(f"Invalid mode: {mode}")
    
    def get_pointer(self, read_pos, mode):
        if read_pos < 0:
            raise Exception(f"Asked to get pointer from invalid position: {read_pos}")
        elif mode == 0:
            return self.read(self.read(read_pos))
        elif mode == 1:
            return self.read(read_pos)
        elif mode == 2:
            return self.read(self.read(read_pos) + self.rel_base)
        else:
            raise Exception(f"Inalid mode: {mode}")

    def read(self, read_pos):
        if read_pos < 0:
            raise Exception(f"Asked to read invalid position {read_pos}")
        elif read_pos > len(self.prog):
            self.prog += [0 for i in range(read_pos - len(self.prog) + 2)]
        return(self.prog[read_pos])
    
    def goto(self, goto_pos):
        if goto_pos < 0:
            raise Exception(f"Asked to goto invalid position {goto_pos}")
        elif goto_pos > len(self.prog):
            self.prog += [0 for i in range(goto_pos - len(self.prog) + 2)]
        self.pos = goto_pos
    
    def step(self, step_num):
        self.goto(self.pos + step_num)

    def get_modes(self, instr, n):
        modes = [instr // 10**(i+2) % 10 for i in range(n)]
        # modes.reverse()
        return modes

    def getmode(self, instr, n):
        return (instr // 10**(n+2)) % 10

    def getparams(self, num):
        # pulls 'num' value/pointers from the program starting at position pos
        # params[0] will always be the instruction
        instr = self.prog[self.pos]
        params = [instr % 100]
        for i in range(num):
            mode = self.getmode(instr,i)
            if mode == 0:
                # mode 0: position mode
                params.append(self.read(self.read(self.pos + i + 1)))
            elif mode == 1:
                # mode 1: immediate mode
                params.append(self.read(self.pos + i + 1))
            elif mode == 2:
                # mode 2: relative mode
                params.append(self.read(self.read(self.pos + i + 1) + self.rel_base))
            else:
                raise Exception(f"Unknown mode: {mode} in instruction {instr} at pos {self.pos}")
        return params

def parse_program(instring):
    return [int(x) for x in instring.strip().split(",")]