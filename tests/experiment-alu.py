import matplotlib.pyplot as plt
from architectures.superscalar_cpu import SuperScalarCPU
from architectures.utils.parser import Program

program_path = "programs/"
# program_names = ["factorial", "scalar_product", "gcd"]
program_names = ["arith_test", "branches_test", "factorial", "scalar_product", "gcd"]
# program_names = ["arith_test", "factorial", "gcd"]
programs = [Program(program_path + name + ".asm") for name in program_names]

max_alu = 5
alu_range = list(range(1, max_alu + 1))
data = {}

for i, program in enumerate(programs):
    data[program_names[i]] = []
    for n in alu_range:
        cpu = SuperScalarCPU(program, n_alu=n)
        cpu.run()
        data[program_names[i]].append(round(cpu.instructions/cpu.clk, 2))

for i, program in enumerate(programs):
    plt.plot(alu_range, data[program_names[i]], label=program_names[i])

plt.xticks(alu_range)
plt.xlabel("Benchmark program used")
plt.ylabel("Instructions per clock cycle")
plt.legend()
plt.title("Performance evolution with the number of ALUs")
plt.show()
print(data)
