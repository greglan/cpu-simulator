INSTR_TYPE_ARITH = 1    # Logical and arith operations
INSTR_TYPE_MEM = 2      # Load and stores
INSTR_TYPE_BRANCH = 4   # Branches


class Instruction:
    def __init__(self, assembly):
        self.opcode = None
        self.operand1 = None
        self.operand2 = None
        self.type = None
        self.parse(assembly)

    def parse(self, assembly):
        """
        Set the members of the class to the given instruction
        :type assembly: str
        :return: None
        """
        if assembly[0] == '#' or assembly == '\n':  # Start with a comment or empty line, so insert NOP
            self.opcode = "nop"
            return

        # Remove any comment
        comment_idx = assembly.find('#')
        if comment_idx != -1:
            assembly = assembly[:comment_idx]

        # Remove trailing chars
        assembly = assembly.strip()

        # Detect syntax
        if assembly.count(',') == 1:  # Comma detected, so 2 operands
            opcode_operand1, operand2 = assembly.split(',')
            opcode, operand1 = opcode_operand1.strip().split(' ')

            self.opcode = opcode.strip()
            self.operand1 = operand1.strip()
            self.operand2 = operand2.strip()
        else:
            try:
                opcode, operand1 = assembly.split(' ')
                self.opcode, self.operand1 = opcode.strip(), operand1.strip()
                self.type = INSTR_TYPE_BRANCH
            except ValueError:
                if "ret" in assembly:
                    self.opcode = "ret"
                    self.type = INSTR_TYPE_BRANCH
                elif "nop" in assembly:
                    self.opcode = "nop"

    def __str__(self):
        s = self.opcode + " "
        if self.operand1 is not None:
            s += self.operand1
            if self.operand2 is not None:
                s += ", " + self.operand2
        return s

    def __repr__(self):
        return self.__str__()


class Program(list):
    def __init__(self, filename):
        super(Program, self).__init__()
        file = open(filename, 'r')

        for line in file:
            self.append(Instruction(line))
        file.close()
