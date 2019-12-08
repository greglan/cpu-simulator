from architectures import N_REG
from architectures.utils.parser import INSTR_TYPE_MEM
from architectures.utils.components import Memory, Stack, RegisterBank, ALU, LoadStoreUnit, BranchUnit
from architectures.pipelines import SuperScalarPipeline


class SuperScalarCPU:
    def __init__(self, program, n_alu=2):
        self.mem = Memory(512)
        self.stack = Stack()
        self.prog = program
        self.clk = 0            # Total number of clock cycles
        self.clk_inc = 0        # Amount of clock cycles to stall the pipeline
        self.stall_count = 0    # Amount of clock cycles to stall
        self.instructions = 0   # Number of instructions executed

        self.reg = RegisterBank(N_REG)
        self.alu = [ALU(self.reg) for alu in range(n_alu)]
        self.lsu = LoadStoreUnit(self.reg, self.mem, self.stack)
        self.bu = BranchUnit(self.reg, self.stack)
        self.alu_ready = n_alu-1
        self.lsu_ready = True
        self.bu_ready = True

        self.pipeline = SuperScalarPipeline(n_alu, self.reg, self.prog)
        self.halted = False

    def run(self):
        while not self.halted:
            if not self.pipeline.exec_stalled:
                # Execute first so that the scoreboard can be updated ~ immediate feedback (bypass)
                pc_modified = self.__exec_instructions()
                self.pipeline.decode()  # Update the next execute state (decode instructions, check for dependencies)
                if not self.pipeline.decode_stalled:
                    # if not pc_modified:
                    self.reg.next["pc"] = self.reg.current["pc"] + self.pipeline.width
                    self.pipeline.fetch()   # Update the next fetch state

                # Sync components
                self.pipeline.sync()
                self.reg.sync()
                self.mem.sync()
                self.stack.sync()
            else:
                self.pipeline.exec_stalled = False  # Reset the flag

            self.clk += 1

    def __exec_instructions(self):
        """
        Execute the instructions in the current "execute" stage of the pipeline.
        Update the exec_stalled flag in the pipeline
        """
        pc_modified = False  # Have executed any branch instruction ?

        for instr in self.pipeline.current["execute"]:
            if instr is None:
                pass
            elif instr.opcode == "nop":
                self.clk -= 1  # Compensate the clock increase
            elif instr.opcode == "mov":
                self.reg.next[instr.op1] = self.reg.current[instr.op2]
            elif instr.opcode == "movi":
                self.reg.next[instr.op1] = int(instr.op2)
            elif instr.opcode == "ldr":
                if instr.op3 is None:
                    self.reg.next[instr.op1] = self.mem.current[self.reg.current[instr.op2]]
                else:
                    self.reg.next[instr.op1] = self.mem.current[self.reg.current[instr.op2] + self.reg.current[instr.op3]]
            elif instr.opcode == "str":
                if instr.op3 is None:
                    self.mem.next[self.reg.current[instr.op2]] = self.reg.current[instr.op1]
                else:
                    self.mem.next[self.reg.current[instr.op2] + self.reg.current[instr.op3]] = self.reg.current[instr.op1]
            elif instr.opcode == "push":
                self.stack.next.append(self.reg.current[instr.op1])
            elif instr.opcode == "pop":
                self.reg.next[instr.op1] = self.stack.next.pop()
            elif instr.opcode == "not":
                self.reg.next[instr.op1] = ~self.reg.current[instr.op2] & 0xffffffff
            elif instr.opcode == "and":
                self.reg.next[instr.op1] = self.reg.current[instr.op1] & self.reg.current[instr.op2]
            elif instr.opcode == "or":
                self.reg.next[instr.op1] = self.reg.current[instr.op1] | self.reg.current[instr.op2]
            elif instr.opcode == "xor":
                self.reg.next[instr.op1] = self.reg.current[instr.op1] ^ self.reg.current[instr.op2]
            elif instr.opcode == "lsl":
                self.reg.next[instr.op1] = self.reg.current[instr.op1] << self.reg.current[instr.op2]
            elif instr.opcode == "lsr":
                self.reg.next[instr.op1] = self.reg.current[instr.op1] >> self.reg.current[instr.op2]
            elif instr.opcode == "add":
                self.reg.next[instr.op1] += self.reg.current[instr.op2]
            elif instr.opcode == "addi":
                self.reg.next[instr.op1] += int(instr.op2)
            elif instr.opcode == "sub":
                self.reg.next[instr.op1] -= self.reg.current[instr.op2]
            elif instr.opcode == "subi":
                self.reg.next[instr.op1] -= int(instr.op2)
            elif instr.opcode == "mul":
                self.reg.next[instr.op1] *= self.reg.current[instr.op2]
            elif instr.opcode == "div":
                self.reg.next[instr.op1] //= self.reg.current[instr.op2]
            elif instr.opcode == "cmp":
                self.reg.next["zflag"] = self.reg.current[instr.op1] == self.reg.current[instr.op2]
                self.reg.next["gflag"] = self.reg.current[instr.op1] > self.reg.current[instr.op2]
            elif instr.opcode == "b":
                self.reg.next["pc"] = int(instr.op1) - 1
                pc_modified = True
                self.pipeline.clear()
            elif instr.opcode == "br":
                self.stack.next.append(self.reg.current["pc"] - 2 + 1 - 1)  # Next (PC-2). But pipeline update in PC+1
                self.reg.next["pc"] = int(instr.op1) - 1
                pc_modified = True
                self.pipeline.clear()
            elif instr.opcode == "ret":
                self.reg.next["pc"] = self.stack.next.pop()
                pc_modified = True
                self.pipeline.clear()
            elif instr.opcode == "be":
                if self.reg.current["zflag"]:
                    self.reg.next["pc"] = int(instr.op1) - 1
                    pc_modified = True
                    self.pipeline.clear()
                    self.reg.next["zflag"] = False
            elif instr.opcode == "bg":
                if self.reg.current["gflag"]:
                    self.reg.next["pc"] = int(instr.op1) - 1
                    pc_modified = True
                    self.pipeline.clear()
                    self.reg.next["gflag"] = False
            elif instr.opcode == "hlt":
                self.halted = True
            else:
                raise Exception("Unknown instruction: %s" % str(instr))

            if (instr is not None) and (instr.type == INSTR_TYPE_MEM):
                self.pipeline.exec_stalled = True

            if (instr is not None) and (instr.opcode != "nop"):
                self.instructions += 1

            self.pipeline.release_instruction_resources(instr)

        return pc_modified

    def __str__(self):
        s = str(self.reg)
        s += "Clock cycles: %d\n" % self.clk
        s += "Number of instructions: %d\n" % self.instructions
        if self.clk != 0:
            s += "Number of instructions per cycle: %.04f\n" % (self.instructions / self.clk)
        return s
