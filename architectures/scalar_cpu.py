from parser import Instruction

N_REG = 13


class ScalarCPU:
    def __init__(self):
        self.mem = Memory(512)
        self.stack = []
        self.clk = 0  # Clock cycles
        self.instructions = 0  # Number of instructions executed

        keys = ["r"+str(i) for i in range(N_REG)]
        self.reg = {key: 0 for key in keys}
        self.pc = 1
        self.zflag = 0  # Zero flag
        self.gflag = 0  # Greater than flag

    def run(self, program):
        eof = len(program)+1
        self.pc = 1

        while self.pc != eof:
            self.eu_exec(program[self.pc-1])

    def eu_exec(self, instr):
        """

        :type instr: Instruction
        """
        if instr.opcode == "nop":
            self.pc += 1
        elif instr.opcode == "mov":
            self.reg[instr.op1] = self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "movi":
            self.reg[instr.op1] = int(instr.op2)
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "ldr":
            if instr.op3 is None:
                self.reg[instr.op1] = self.mem[self.reg[instr.op2]]
            else:
                self.reg[instr.op1] = self.mem[self.reg[instr.op2] + self.reg[instr.op3]]
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "str":
            if instr.op3 is None:
                self.mem[self.reg[instr.op2]] = self.reg[instr.op1]
            else:
                self.mem[self.reg[instr.op2] + self.reg[instr.op3]] = self.reg[instr.op1]
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "push":
            self.stack.append(self.reg[instr.op1])
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "pop":
            self.reg[instr.op1] = self.stack.pop()
            self.clk += 2
            self.pc += 1
        elif instr.opcode == "not":
            self.reg[instr.op1] = ~self.reg[instr.op2] & 0xffffffff
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "and":
            self.reg[instr.op1] = self.reg[instr.op1] & self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "or":
            self.reg[instr.op1] = self.reg[instr.op1] | self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "xor":
            self.reg[instr.op1] = self.reg[instr.op1] ^ self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "lsl":
            self.reg[instr.op1] = self.reg[instr.op1] << self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "lsr":
            self.reg[instr.op1] = self.reg[instr.op1] >> self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "add":
            self.reg[instr.op1] += self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "addi":
            self.reg[instr.op1] += int(instr.op2)
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "sub":
            self.reg[instr.op1] -= self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "subi":
            self.reg[instr.op1] -= int(instr.op2)
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "mul":
            self.reg[instr.op1] *= self.reg[instr.op2]
            self.clk += 3
            self.pc += 1
        elif instr.opcode == "div":
            self.reg[instr.op1] //= self.reg[instr.op2]
            self.clk += 3
            self.pc += 1
        elif instr.opcode == "cmp":
            self.zflag = self.reg[instr.op1] == self.reg[instr.op2]
            self.gflag = self.reg[instr.op1] > self.reg[instr.op2]
            self.clk += 1
            self.pc += 1
        elif instr.opcode == "b":
            self.clk += 3
            self.pc = int(instr.op1)
        elif instr.opcode == "br":
            self.clk += 3
            self.stack.append(self.pc + 1)
            self.pc = int(instr.op1)
        elif instr.opcode == "ret":
            self.clk += 3
            self.pc = self.stack.pop()
        elif instr.opcode == "be":
            self.clk += 3  # FIXME: move that into the if-else ?
            if self.zflag:
                self.pc = int(instr.op1)
                self.zflag = False
            else:
                self.pc += 1
        elif instr.opcode == "bg":
            self.clk += 3  # FIXME: move that into the if-else ?
            if self.gflag:
                self.pc = int(instr.op1)
                self.gflag = False
            else:
                self.pc += 1
        else:
            raise Exception("Unknown instruction: %s" % str(instr))

        if instr.opcode != "nop":
            self.instructions += 1

    def __str__(self):
        s = ""
        for reg in range(N_REG):
            reg_str = "r%d" % reg
            s += "%s: 0x%x\n" % (reg_str, self.reg[reg_str])
        s += "pc: %d\n" % self.pc
        s += "Clock cycles: %d\n" % self.clk
        s += "Number of instructions: %d\n" % self.instructions
        s += "Number of instructions per cycle: %.04f\n" % (self.instructions/self.clk)
        return s


class Memory(list):
    def __init__(self, size):
        super(Memory, self).__init__()
        self.size = size
        for i in range(size):
            self.append(0)
