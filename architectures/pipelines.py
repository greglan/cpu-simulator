from architectures.utils.parser import Instruction


class FetchDecodeExecutePipeline:
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
