import unittest

from intcode2 import Intcode, parse_program, readfile

TESTSDIR = "/home/richard/python/advent-of-code/tests/"


class TestIntcode(unittest.TestCase):
    def test_readfile(self):
        self.assertEqual(readfile(TESTSDIR + "basic_99.txt"), "99")

    def test_parser(self):
        self.assertEqual(parse_program(readfile(TESTSDIR + "basic_99.txt")),
                         [99])

    def test_parser2(self):
        self.assertEqual(
                parse_program(readfile(TESTSDIR + "basic_99_with_memory.txt")),
                [99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_get_modes(self):
        m = Intcode([])
        self.assertEqual(m.get_modes(12001, 4), [0, 2, 1, 0])

    def test_opcode_1_1(self):
        m = Intcode([1, 5, 6, 7, 99, 10, 12, 0, 0, 0])
        m.run()
        self.assertEqual(m.prog, [1, 5, 6, 7, 99, 10, 12, 22, 0, 0])

    def test_opcode_1_2(self):
        m = Intcode([101, 5, 6, 7, 99, 10, 12, 0, 0, 0])
        m.run()
        self.assertEqual(m.prog, [101, 5, 6, 7, 99, 10, 12, 17, 0, 0])

    def test_opcode_1_3(self):
        m = Intcode([1001, 5, 6, 7, 99, 10, 12, 0, 0, 0])
        m.run()
        self.assertEqual(m.prog, [1001, 5, 6, 7, 99, 10, 12, 16, 0, 0])

    def test_opcode_1_4(self):
        m = Intcode([1101, 5, 6, 7, 99, 10, 12, 0, 0, 0])
        m.run()
        self.assertEqual(m.prog, [1101, 5, 6, 7, 99, 10, 12, 11, 0, 0])

    def test_week_2_1(self):
        m = Intcode(parse_program(readfile(TESTSDIR + "2_test_1.txt")))
        m.run()
        self.assertEqual(
                [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
                m.prog)

    def test_week_2_2(self):
        m = Intcode([1, 0, 0, 0, 99])
        m.run()
        self.assertEqual([2, 0, 0, 0, 99], m.prog)

    def test_week_2_3(self):
        m = Intcode([2, 3, 0, 3, 99])
        m.run()
        self.assertEqual([2, 3, 0, 6, 99], m.prog)

    def test_week_2_4(self):
        m = Intcode([2, 4, 4, 5, 99, 0])
        m.run()
        self.assertEqual([2, 4, 4, 5, 99, 9801], m.prog)

    def test_week_2_5(self):
        m = Intcode([1, 1, 1, 4, 99, 5, 6, 0, 99])
        m.run()
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], m.prog)

    def test_week_5_1(self):
        m = Intcode([3, 0, 4, 0, 99])
        self.assertEqual(m.run([17]), [17, None])

    def test_week_5_2(self):
        m = Intcode([1002, 4, 3, 4, 33])
        m.run()
        self.assertEqual([1002, 4, 3, 4, 99], m.prog)

    def test_8_1(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(readfile(TESTSDIR + "8_test_1.txt")))
            expect = (1 if n == 8 else 0)
            self.assertEqual(m.run([n]), [expect, None])

    def test_8_2(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(readfile(TESTSDIR + "8_test_2.txt")))
            expect = (1 if n < 8 else 0)
            self.assertEqual(m.run([n]), [expect, None])

    def test_8_3(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(readfile(TESTSDIR + "8_test_3.txt")))
            expect = (1 if n == 8 else 0)
            self.assertEqual(m.run([n]), [expect, None])

    def test_8_4(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(readfile(TESTSDIR + "8_test_4.txt")))
            expect = (1 if n < 8 else 0)
            self.assertEqual(m.run([n]), [expect, None])

    def test_zero_pos_mode(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(
                readfile(TESTSDIR + "zero_pos_mode.txt")))
            expect = (0 if n == 0 else 1)
            self.assertEqual(m.run([n]), [expect, None])

    def test_zero_imm_mode(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(
                readfile(TESTSDIR + "zero_imm_mode.txt")))
            expect = (0 if n == 0 else 1)
            self.assertEqual(m.run([n]), [expect, None])

    def test_8_5(self):
        for n in [-1000, -1, 0, 1, 5, 7, 8, 9, 1000]:
            m = Intcode(parse_program(readfile(TESTSDIR + "8_test_5.txt")))
            if n < 8:
                expect = 999
            elif n == 8:
                expect = 1000
            else:
                expect = 1001
            self.assertEqual(m.run([n]), [expect, None])

    # def write_extend_test(self):
    #     m = Intcode[1101,2,3,100]
    #     m.run()

    def test_9_1(self):
        prog = parse_program(readfile(TESTSDIR + "9_test_1.txt"))
        m = Intcode(prog)
        self.assertEqual(m.run(), prog + [None])

    def test_9_2(self):
        m = Intcode(parse_program(readfile(TESTSDIR + "9_test_2.txt")))
        self.assertGreaterEqual(m.run()[0], 10**15)
    
    def test_9_3(self):
        prog = [104, 1125899906842624, 99]
        m = Intcode(prog)
        self.assertEqual(m.run()[0], prog[1])

if __name__ == "__main__":
    unittest.main()
