from unittest import TestCase
from parser import *


class TestParser(TestCase):
    def test_instr_parsing(self):
        str_instr = "sub r1, r0"
        str_instr = "sub r1, r0  # Comment"
        instr = Instruction(str_instr)
        print("(%s, %s, %s)" % (instr.opcode, instr.operand1, instr.operand2))
        self.assertTrue(True)

    def test_program_parsing(self):
        prog = Program("programs/arith_test.asm")
        # prog = Program("programs/branches_test.asm")

        print("Program has %d lines" % len(prog))
        for instruction in prog:
            print("(%s, %s, %s)" % (instruction.opcode, instruction.operand1, instruction.operand2))

        self.assertTrue(True)
