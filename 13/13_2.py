from intcode2 import readfile, parse_program, Intcode
from numpy import sign
from time import sleep

SPRITES = {0: "   ", 1: "+++", 2: "[%]", 3: "---", 4: "(O)"}
KEYMAP = {"a": -1, "s": 0, "d": 1, "q": 9}

class Game:
    def __init__(self, raw_out):
        raw_objs = [raw_out[i:i+3] for i in range(0, len(raw_out) - 1, 3)]
        self.width = max([obj[0] for obj in raw_objs])
        self.height = max([obj[1] for obj in raw_objs])

        self.screen = []
        for y in range(self.height + 1):
            self.screen.append(["" for x in range(self.width + 1)])
        self.score = 0

        for obj in raw_objs:
            (x, y) = (obj[0], obj[1])
            self.screen[y][x] = obj[2]
            if obj[2] == 3:
                self.paddle_xpos = x
            elif obj[2] == 4:
                self.ball_xpos = x
    
    def display(self):
        print(f"Score: {self.score}")
        for row in self.screen:
            # print(f"row: {row}")
            print("".join([SPRITES[obj] for obj in row]))
        
    def update(self, raw_out):
        raw_objs = [raw_out[i:i+3] for i in range(0, len(raw_out) - 1, 3)]
        for obj in raw_objs:
            (x, y) = (obj[0], obj[1])
            if x == -1:
                self.score = obj[2]
            else:
                self.screen[y][x] = obj[2]
                if obj[2] == 3:
                    self.paddle_xpos = x
                elif obj[2] == 4:
                    self.ball_xpos = x

machine = Intcode(parse_program(readfile("input2.txt")))

# initial run
user_input = 0
game = Game(machine.run([user_input]))
while user_input != 9:
    machine_output = machine.run([user_input])
    if machine_output == [None]:
        print(f"Game over! Final score: {game.score}")
        exit()
    game.update(machine_output)
    # game.display()

    # user playing
    # raw_in = ""
    # while raw_in not in KEYMAP.keys():
    #     raw_in = input("Input: (A=left, D=right, S=stay, Q=quit):").lower()
    # user_input = KEYMAP[raw_in]

    # computer player
    user_input = sign(game.ball_xpos - game.paddle_xpos)
