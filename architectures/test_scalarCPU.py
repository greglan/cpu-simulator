from unittest import TestCase
from architectures.scalar_cpu import ScalarCPU
from parser import Program


class TestScalarCPU(TestCase):
    def test_run(self):
        cpu = ScalarCPU()

        prog = Program("programs/arith_test.asm")
        cpu.run(prog)
        self.assertEqual(cpu.reg['r0'], 0)
        self.assertEqual(cpu.reg['r2'], 0x7d0)
        self.assertEqual(cpu.reg['r3'], 1)
        self.assertEqual(cpu.reg['r7'], 2**32-1-2)
        self.assertEqual(cpu.reg['r8'], 2)
        self.assertEqual(cpu.reg['r9'], 16)
        self.assertEqual(cpu.reg['r10'], 1)

        # prog = Program("programs/branches_test.asm")
        # print(cpu)

        prog = Program("programs/mem_test.asm")
        cpu.run(prog)
        self.assertEqual(cpu.reg['r3'], 0xfe01)

        prog = Program("programs/factorial.asm")
        cpu.run(prog)
        self.assertEqual(cpu.reg['r0'], 720)

        prog = Program("programs/scalar_product.asm")
        cpu.run(prog)
        self.assertEqual(cpu.reg['r3'], 0x7f80)

        # print(cpu)

