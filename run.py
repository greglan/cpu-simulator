from parser import Program
from architectures.scalar_cpu import ScalarCPU


def main():
    # prog = Program("programs/arith_test.asm")
    prog = Program("programs/branches_test.asm")
    # prog = Program("programs/mem_test.asm")
    # prog = Program("programs/factorial.asm")
    # prog = Program("programs/scalar_product.asm")
    cpu = ScalarCPU()
    cpu.run(prog)
    print(cpu)


if __name__ == "__main__":
    main()
