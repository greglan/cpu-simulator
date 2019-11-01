from queue import Queue
N_REG = 13


class ScalarCPU:
    def __init__(self):
        self.eu = ExecutionUnit()
        memory = Memory(512)

    def run(self, program):
        memory = Memory(512)
        self.eu.execute_prog(program, memory)

    def __str__(self):
        s = ""
        for reg in range(N_REG):
            reg_str = "r%d" % reg
            s += "%s: 0x%x\n" % (reg_str, self.eu.reg[reg_str])
        s += "pc: %d\n" % self.eu.pc
        s += "Clock cycles: %d\n" % self.eu.clk
        s += "Number of instructions: %d\n" % self.eu.instructions
        s += "Number of instructions per cycle: %.04f\n" % (self.eu.instructions/self.eu.clk)
        return s


class ExecutionUnit:
    def __init__(self, n_reg=N_REG):
        self.reg = [0 for i in range(n_reg)]
        keys = ["r"+str(i) for i in range(n_reg)]
        self.reg = {key: 0 for key in keys}
        self.pc = 1
        self.zflag = 0  # Zero flag
        self.gflag = 0  # Greater than flag
        self.stack = []
        self.clk = 0  # Clock cycles
        self.instructions = 0  # Number of instructions executed

    def execute_prog(self, prog, mem=None):
        eof = len(prog)+1
        self.pc = 1

        while self.pc != eof:
            self.execute(prog[self.pc-1], mem=mem)

    def execute(self, instr, mem=None):
        if instr.opcode == "nop":
            self.pc += 1
        elif instr.opcode == "mov":
            self.reg[instr.operand1] = self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "movi":
            self.reg[instr.operand1] = int(instr.operand2)
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "ldr":
            self.reg[instr.operand1] = mem[self.reg[instr.operand2]]
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "str":
            mem[self.reg[instr.operand2]] = self.reg[instr.operand1]
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "push":
            self.stack.append(self.reg[instr.operand1])
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "pop":
            self.reg[instr.operand1] = self.stack.pop()
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "not":
            self.reg[instr.operand1] = ~self.reg[instr.operand2] & 0xffffffff
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "and":
            self.reg[instr.operand1] = self.reg[instr.operand1] & self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "or":
            self.reg[instr.operand1] = self.reg[instr.operand1] | self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "xor":
            self.reg[instr.operand1] = self.reg[instr.operand1] ^ self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "add":
            self.reg[instr.operand1] += self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "addi":
            self.reg[instr.operand1] += int(instr.operand2)
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "sub":
            self.reg[instr.operand1] -= self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "subi":
            self.reg[instr.operand1] -= int(instr.operand2)
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "mul":
            self.reg[instr.operand1] *= self.reg[instr.operand2]
            self.clk += 3
            self.pc += 1
        elif instr.opcode == "div":
            self.reg[instr.operand1] //= self.reg[instr.operand2]
            self.clk += 3
            self.pc += 1
        elif instr.opcode == "cmp":
            self.zflag = self.reg[instr.operand1] == self.reg[instr.operand2]
            self.gflag = self.reg[instr.operand1] > self.reg[instr.operand2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "b":
            self.clk += 3
            self.pc = int(instr.operand1)
        elif instr.opcode == "br":
            self.clk += 3
            self.stack.append(self.pc + 1)
            self.pc = int(instr.operand1)
        elif instr.opcode == "ret":
            self.clk += 3
            self.pc = self.stack.pop()
        elif instr.opcode == "be":
            self.clk += 3  # FIXME: move that into the if-else ?
            if self.zflag:
                self.pc = int(instr.operand1)
                self.zflag = False
            else:
                self.pc += 1
        elif instr.opcode == "bg":
            self.clk += 3  # FIXME: move that into the if-else ?
            if self.gflag:
                self.pc = int(instr.operand1)
                self.gflag = False
            else:
                self.pc += 1
        else:
            raise Exception("Unknown instruction: %s" % str(instr))

        if instr.opcode != "nop":
            self.instructions += 1


class Memory(list):
    def __init__(self, size):
        super(Memory, self).__init__()
        self.size = size
        for i in range(size):
            self.append(0)
