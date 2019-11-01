from unittest import TestCase
from architectures.scalar_cpu import ScalarCPU
from parser import Program


class TestScalarCPU(TestCase):
    def test_run(self):
        # prog = Program("programs/arith_test.asm")
        # prog = Program("programs/branches_test.asm")
        # prog = Program("programs/mem_test.asm")
        # prog = Program("programs/factorial.asm")
        prog = Program("programs/scalar_product.asm")
        cpu = ScalarCPU()
        cpu.run(prog)
        print(cpu)

