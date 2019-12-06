from unittest import TestCase
from architectures.utils.parser import *


class TestParser(TestCase):
    def test_instr_parsing(self):
        # str_instr = "sub r1, r0"
        str_instr = "sub r1, r0  # Comment"
        instr = Instruction(str_instr)
        self.assertEqual("sub r1, r0", str(instr))
        # print("(%s, %s, %s)" % (instr.opcode, instr.op1, instr.op2))

        str_instr = "ldr r0, r1, r4  # Comment"
        instr = Instruction(str_instr)
        self.assertEqual("r4", instr.op3)
        self.assertEqual("ldr r0, r1, r4", str(instr))

        str_instr = "ret  # Comment"
        instr = Instruction(str_instr)
        self.assertEqual(None, instr.op1)
        self.assertEqual(None, instr.op2)
        self.assertEqual(None, instr.op3)
        self.assertEqual("ret", str(instr))

        str_instr = "wait"
        instr = Instruction(str_instr)
        self.assertEqual(None, instr.op1)
        self.assertEqual(None, instr.op2)
        self.assertEqual(None, instr.op3)
        self.assertEqual("wait", str(instr))

    def test_program_parsing(self):
        # prog = Program("programs/arith_test.asm")
        # prog = Program("programs/branches_test.asm")
        prog = Program("programs/mem_test.asm")

        print("Program has %d lines" % len(prog))
        for instruction in prog:
            print("(%s, %s, %s, %s)" % (instruction.opcode, instruction.op1, instruction.op2, instruction.op3))

        self.assertTrue(True)
