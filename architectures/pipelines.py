from architectures.utils.parser import *


class SimplePipeline:
    def __init__(self):
        self.current = dict()
        self.next = dict()
        self.current["fetch"] = Instruction("wait")    # Instruction located at reg.current["pc"]
        self.current["decode"] = Instruction("wait")   # Currently does nothing, but will involve branch predictor later
        self.current["execute"] = Instruction("wait")  # Contains an instruction
        self.next["fetch"] = Instruction("wait")
        self.next["decode"] = Instruction("wait")
        self.next["execute"] = Instruction("wait")

    def clear(self):
        self.current["fetch"] = Instruction("wait")    # Instruction located at reg.current["pc"]
        self.current["decode"] = Instruction("wait")   # Currently does nothing, but will involve branch predictor later
        self.current["execute"] = Instruction("wait")  # Contains an instruction
        self.next["fetch"] = Instruction("wait")
        self.next["decode"] = Instruction("wait")
        self.next["execute"] = Instruction("wait")

    def update(self):
        """
        Set the current state to the next
        :return: None
        """
        for stage in ["fetch", "decode", "execute"]:
            self.current[stage] = self.next[stage]


class SuperScalarPipeline:
    def __init__(self, width, register_bank, program):
        """
        Possible super-scalar pipeline states:
        * Normal operation:
            [F] [D] [ ]
            [ ] [F] [D]
        * Decode stall operation:
            [F] [D] [ ]
            [F] [D] [D]
        * Execute stall operation (ldr/str/push/pop):
            [F] [D] [E]
            [F] [D] [E]
          FIXME: in this case, can we still advance the decode to the execute stage ?
        """
        self.width = width
        self.reg = register_bank
        self.program = program
        self.current = dict()
        self.next = dict()
        self.decode_stalled = False    # Indicate if the pipeline should update as normal or stall
        self.exec_stalled = False   # Indicate whether the current "execute" stage contain memory instruction

        self.alu_ready = self.width - 1
        self.lsu_ready = True
        self.bu_ready = True

        stages = ["fetch", "decode", "execute"]

        for stage in stages:
            self.current[stage] = [None for instruction in range(width)]
            self.next[stage] = [None for instruction in range(width)]

    def fetch(self):
        """
        Update the next fetch state by fetching *width* instructions from the program memory
        :return: None
        """
        for i in range(self.width):
            # pc + i may be out of range. Fix it by padding with None instructions
            instr_addr = self.reg.current["pc"] + i
            if instr_addr < self.program.end:   # pc + i in range
                self.next["fetch"][i] = self.program[self.reg.current["pc"] + i]
            else:
                self.next["fetch"][i] = None    # Padding

    def decode(self):
        """
        Update the next execute state and check for dependencies. Uses issue blockage.
        If there is a dependency, stall, i.e do not copy instructions to the execute stage.
        Once dependencies are resolved, determine if there is enough UE to issue the instructions
        :return: None
        """
        self.alu_ready = self.width - 1
        self.lsu_ready = True
        self.bu_ready = True
        instructions = self.current["fetch"]
        ready_instructions = []    # List of instruction to issue to the "execute" stage

        # Compute dependencies
        for i, instruction in enumerate(instructions):
            if self.__check_instruction_ready(instruction):
                self.__lock_instruction_resources(instruction)
                ready_instructions.append((i, instruction))
            else:
                break   # Necessary for in-order issue

        # Check that there is enough UEs
        issued_instructions = []    # List of instruction to issue to the "execute" stage
        for (i, instr) in ready_instructions:
            if instr is None:
                # TODO: add statistics
                pass
            elif instr.type == INSTR_TYPE_ALU and self.alu_ready > 0:
                issued_instructions.append((i, instr))
                self.alu_ready -= 1
            elif instr.type == INSTR_TYPE_MEM and self.lsu_ready:
                issued_instructions.append((i, instr))
                self.lsu_ready = False
            elif self.bu_ready:
                issued_instructions.append((i, instr))
                self.bu_ready = False
            else:
                break   # Necessary for in-order issue

        # Update the stall indicator
        self.decode_stalled = len(instructions) != len(issued_instructions)

        # If only some of the instructions can be executed, create a custom "fetch" and "decode" stage
        if self.decode_stalled:
            self.next["fetch"] = self.current["fetch"]  # Stall fetch stage

            # Replace issued instructions from the "decode" stage by None
            self.__reset_next_stage("decode")   # Init to None
            for i, instruction in enumerate(instructions):
                if (i, instruction) not in issued_instructions:  # Add unissued instructions
                    self.next["decode"][i] = instruction

        # Update the next execute stage
        self.__reset_next_stage("execute")
        for (i, issued_instruction) in issued_instructions:
            self.next["execute"][i] = issued_instruction

    def __check_instruction_ready(self, instruction):
        """
        Check that all operands are ready in the scoreboard.
        Use the list of non-None operands
        :return: bool
        """
        if instruction is None:
            return True

        table = self.reg.scoreboard
        ready = True
        for operand in instruction.operands:
            ready = ready and table[operand]
        return ready

    def __lock_instruction_resources(self, instruction):
        """
        Use the list of non-None operands
        """
        if instruction is None:
            return

        table = self.reg.scoreboard
        for operand in instruction.operands:
            table[operand] = False

    def release_instruction_resources(self, instruction):
        """
        Use the list of non-None operands
        """
        if instruction is None:
            return

        table = self.reg.scoreboard
        for operand in instruction.operands:
            table[operand] = True

    def __reset_next_stage(self, stage):
        self.next[stage] = [None for instruction in range(self.width)]

    def clear(self):
        self.decode_stalled = False
        stages = ["fetch", "decode", "execute"]

        for stage in stages:
            self.current[stage] = [None for instruction in range(self.width)]
            self.next[stage] = [None for instruction in range(self.width)]

    def update(self):
        """
        Set the current state to the next
        :return: None
        """
        self.current["execute"] = self.next["execute"]
        self.current["decode"] = self.current["fetch"]
        self.current["fetch"] = self.next["fetch"]

    def sync(self):
        self.update()
