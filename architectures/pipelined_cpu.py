from architectures.utils import N_REG
from architectures.utils.components import Memory, Stack, RegisterBank
from architectures.pipelines import FetchDecodeExecutePipeline


class PipelinedCPU:
    def __init__(self):
        self.mem = Memory(512)
        self.stack = Stack()
        self.prog = None
        self.clk = 0  # Clock cycles
        self.clk_inc = 0  # Amount of clock cycles to stall the pipeline
        self.instructions = 0  # Number of instructions executed

        self.pipeline = FetchDecodeExecutePipeline()
        self.reg = RegisterBank(N_REG)
        self.halted = False

    def run(self, program):
        self.mem = Memory(512)
        self.stack = Stack()
        self.prog = program
        self.pipeline.clear()
        self.reg.clear()
        self.halted = False
        self.clk = 0  # Clock cycles
        self.clk_inc = 0  # Amount of clock cycles to stall the pipeline
        self.instructions = 0  # Number of instructions executed

        while not self.halted:
            self.advance_clock()

    def advance_clock(self):
        # Compute the next states
        self.__pipeline_fetch()
        self.__pipeline_decode()
        self.__pipeline_exec(self.pipeline.current["execute"])

        # Set the next states as the current states
        self.reg.update()
        self.mem.update()
        self.stack.update()
        self.pipeline.next["execute"] = self.pipeline.current["decode"]
        self.pipeline.next["decode"] = self.pipeline.current["fetch"]
        self.pipeline.update()

        self.clk += self.clk_inc

    def __pipeline_fetch(self):
        pc = self.reg.current["pc"]
        if pc < self.prog.end:
            self.pipeline.next["fetch"] = self.prog[pc]

    def __pipeline_decode(self):
        # In this simple pipeline, decoding does not do anything. Just copy the instruction
        self.pipeline.next["decode"] = self.pipeline.current["fetch"]

    def __pipeline_exec(self, instr):
        if instr.opcode == "nop":
            self.reg.next["pc"] = self.reg.current["pc"] + 1
        elif instr.opcode == "mov":
            self.reg.next[instr.op1] = self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "movi":
            self.reg.next[instr.op1] = int(instr.op2)
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "ldr":
            if instr.op3 is None:
                self.reg.next[instr.op1] = self.mem.current[self.reg.current[instr.op2]]
            else:
                self.reg.next[instr.op1] = self.mem.current[self.reg.current[instr.op2] + self.reg.current[instr.op3]]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 2
        elif instr.opcode == "str":
            if instr.op3 is None:
                self.mem.next[self.reg.current[instr.op2]] = self.reg.current[instr.op1]
            else:
                self.mem.next[self.reg.current[instr.op2] + self.reg.current[instr.op3]] = self.reg.current[instr.op1]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 2
        elif instr.opcode == "push":
            self.stack.next.append(self.reg.current[instr.op1])
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 2
        elif instr.opcode == "pop":
            self.reg.next[instr.op1] = self.stack.next.pop()
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 2
        elif instr.opcode == "not":
            self.reg.next[instr.op1] = ~self.reg.current[instr.op2] & 0xffffffff
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "and":
            self.reg.next[instr.op1] = self.reg.current[instr.op1] & self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "or":
            self.reg.next[instr.op1] = self.reg.current[instr.op1] | self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "xor":
            self.reg.next[instr.op1] = self.reg.current[instr.op1] ^ self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "lsl":
            self.reg.next[instr.op1] = self.reg.current[instr.op1] << self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "lsr":
            self.reg.next[instr.op1] = self.reg.current[instr.op1] >> self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "add":
            self.reg.next[instr.op1] += self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "addi":
            self.reg.next[instr.op1] += int(instr.op2)
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "sub":
            self.reg.next[instr.op1] -= self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "subi":
            self.reg.next[instr.op1] -= int(instr.op2)
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "mul":
            self.reg.next[instr.op1] *= self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 3
        elif instr.opcode == "div":
            self.reg.next[instr.op1] //= self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 3
        elif instr.opcode == "cmp":
            self.reg.next["zflag"] = self.reg.current[instr.op1] == self.reg.current[instr.op2]
            self.reg.next["gflag"] = self.reg.current[instr.op1] > self.reg.current[instr.op2]
            self.reg.next["pc"] = self.reg.current["pc"] + 1
            self.clk_inc = 1
        elif instr.opcode == "b":
            self.reg.next["pc"] = int(instr.op1) - 1
            self.pipeline.clear()
            self.clk_inc = 3
        elif instr.opcode == "br":
            self.stack.next.append(self.reg.current["pc"] - 2 + 1 - 1)  # Next (PC-2). But pipeline update in PC+1
            self.reg.next["pc"] = int(instr.op1) - 1
            self.pipeline.clear()
            self.clk_inc = 3
        elif instr.opcode == "ret":
            self.reg.next["pc"] = self.stack.next.pop()
            self.pipeline.clear()
            self.clk_inc = 3
        elif instr.opcode == "be":
            if self.reg.current["zflag"]:
                self.reg.next["pc"] = int(instr.op1) - 1
                self.pipeline.clear()
                self.reg.next["zflag"] = False
                self.clk_inc = 3
            else:
                self.reg.next["pc"] = self.reg.current["pc"] + 1
                self.clk_inc = 1
        elif instr.opcode == "bg":
            if self.reg.current["gflag"]:
                self.reg.next["pc"] = int(instr.op1) - 1
                self.pipeline.clear()
                self.reg.next["gflag"] = False
                self.clk_inc = 3
            else:
                self.reg.next["pc"] = self.reg.current["pc"] + 1
                self.clk_inc = 1
        elif instr.opcode == "hlt":
            self.halted = True
        else:
            raise Exception("Unknown instruction: %s" % str(instr))

        if instr.opcode != "nop":
            self.instructions += 1

    def __str__(self):
        s = str(self.reg)
        s += "Clock cycles: %d\n" % self.clk
        s += "Number of instructions: %d\n" % self.instructions
        if self.clk != 0:
            s += "Number of instructions per cycle: %.04f\n" % (self.instructions / self.clk)
        return s
