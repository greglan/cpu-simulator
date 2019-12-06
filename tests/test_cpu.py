from unittest import TestCase
from architectures.scalar_cpu import ScalarCPU
from architectures.pipelined_cpu import PipelinedCPU
from architectures.utils.parser import Program


class TestCPU(TestCase):
    def test_scalar_cpu(self):
        cpu = ScalarCPU()
        # self.__test(cpu)

    def test_pipelined_cpu(self):
        cpu = PipelinedCPU()
        self.__test(cpu)

    def __test(self, cpu):
        # prog = Program("programs/gcd.asm")
        # cpu.run(prog)
        # print(cpu)

        # prog = Program("programs/arith_test.asm")
        # cpu.run(prog)
        # self.assertEqual(0, cpu.reg.current['r0'])
        # self.assertEqual(0x7d0, cpu.reg.current['r2'])
        # self.assertEqual(cpu.reg.current['r3'], 1)
        # self.assertEqual(cpu.reg.current['r7'], 2**32-1-2)
        # self.assertEqual(cpu.reg.current['r8'], 2)
        # self.assertEqual(cpu.reg.current['r9'], 16)
        # self.assertEqual(cpu.reg.current['r10'], 1)

        # prog = Program("programs/branches_test.asm")
        # cpu.run(prog)
        # self.assertEqual(0, cpu.reg.current["r0"])
        # print(cpu)

        # prog = Program("programs/mem_test.asm")
        # cpu.run(prog)
        # print(cpu)
        # self.assertEqual(0xfe01, cpu.reg.current['r3'])

        prog = Program("programs/factorial.asm")
        cpu.run(prog)
        print(cpu)
        self.assertEqual(720, cpu.reg.current['r0'])

        prog = Program("programs/scalar_product.asm")
        cpu.run(prog)
        self.assertEqual(0x7f80, cpu.reg.current['r3'])
