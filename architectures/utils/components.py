class Memory:
    def __init__(self, size):
        self.size = size
        self.current = []
        self.next = []
        for i in range(size):
            self.current.append(0)
            self.next.append(0)

    def update(self):
        """
        Update the current state to the next
        :return: None
        """
        for cell in range(self.size):
            self.current[cell] = self.next[cell]


class Stack:
    def __init__(self):
        self.current = []
        self.next = []

    def update(self):
        """
        Update the current state to the next
        :return: None
        """
        self.current = [val for val in self.next]


class RegisterBank:
    def __init__(self, n_regs):
        self.reg_keys = ["r" + str(i) for i in range(n_regs)] + ["pc", "zflag", "gflag"]
        self.n_regs = n_regs + 3  # Add pc, zero flag and greater than flag
        self.current = {key: 0 for key in self.reg_keys}
        self.next = {key: 0 for key in self.reg_keys}

    def clear(self):
        self.current = {key: 0 for key in self.reg_keys}
        self.next = {key: 0 for key in self.reg_keys}

    def update(self):
        """
        Set the current state to the next
        :return: None
        """
        for reg in self.reg_keys:
            self.current[reg] = self.next[reg]

    def __str__(self):
        s = "Current\t\t\t\tNext\n"

        # Iterate over the general purpose registers
        for gp_reg in range(self.n_regs-3):
            s += "%s: 0x%08x\n" % ("r%02d" % gp_reg, self.current["r%d" % gp_reg])

        # Other registers
        s += "pc: 0x%x\n" % self.current["pc"]
        s += "zflag: 0x%x\n" % self.current["zflag"]
        s += "gflag: 0x%x\n" % self.current["zflag"]

        return s

    def __repr__(self):
        s = "Current\t\t\t\tNext\n"

        # Iterate over the general purpose registers
        for gp_reg in range(self.n_regs-3):
            s += "%s: 0x%08x\t\t" % ("r%02d" % gp_reg, self.current["r%d" % gp_reg])
            s += "%s: 0x%08x\n" % ("r%02d" % gp_reg, self.next["r%d" % gp_reg])

        # Other registers
        s += "pc: 0x%x\t\t\tpc: 0x%x\n" % (self.current["pc"], self.next["pc"])
        s += "zflag: 0x%x\t\t\tzflag: 0x%x\n" % (self.current["zflag"], self.next["zflag"])
        s += "gflag: 0x%x\t\t\tgflag: 0x%x\n" % (self.current["gflag"], self.next["gflag"])
        return s
