from architectures.utils.parser import Instruction


class FetchDecodeExecutePipeline:
    def __init__(self):
        self.current = dict()
        self.next = dict()
        self.current["fetch"] = Instruction("nop")    # Instruction located at reg.current["pc"]
        self.current["decode"] = Instruction("nop")   # Currently does nothing, but will involve branch predictor later
        self.current["execute"] = Instruction("nop")  # Contains an instruction
        self.next["fetch"] = Instruction("nop")
        self.next["decode"] = Instruction("nop")
        self.next["execute"] = Instruction("nop")

    def clear(self):
        self.current["fetch"] = Instruction("nop")    # Instruction located at reg.current["pc"]
        self.current["decode"] = Instruction("nop")   # Currently does nothing, but will involve branch predictor later
        self.current["execute"] = Instruction("nop")  # Contains an instruction
        self.next["fetch"] = Instruction("nop")
        self.next["decode"] = Instruction("nop")
        self.next["execute"] = Instruction("nop")

    def update(self):
        """
        Set the current state to the next
        :return: None
        """
        for stage in ["fetch", "decode", "execute"]:
            self.current[stage] = self.next[stage]
