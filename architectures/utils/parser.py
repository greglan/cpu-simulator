INSTR_TYPE_ARITH = 1    # Logical and arith operations
INSTR_TYPE_MEM = 2      # Load and stores
INSTR_TYPE_BRANCH = 4   # Branches


class Instruction:
    def __init__(self, assembly):
        self.opcode = None
        self.op1 = None
        self.op2 = None
        self.op3 = None
        self.type = None
        self.parse(assembly)

    def parse(self, assembly):
        """
        Set the members of the class to the given instruction
        :type assembly: str
        :return: None
        """
        if assembly[0] == '#' or assembly == '\n':  # Start with a comment or empty line, so insert WAIT
            self.opcode = "wait"
            return

        # Remove any comment
        comment_idx = assembly.find('#')
        if comment_idx != -1:
            assembly = assembly[:comment_idx]

        # Remove trailing chars
        assembly = assembly.strip()

        # Detect syntax
        comma_count = assembly.count(',')
        if comma_count == 1:  # Comma detected, so 2 operands
            opcode_operand1, operand2 = assembly.split(',')
            opcode, operand1 = opcode_operand1.strip().split(' ')

            self.opcode = opcode.strip()
            self.op1 = operand1.strip()
            self.op2 = operand2.strip()

        elif comma_count == 2:  # 3 operands
            opcode_operand1, operand2, operand3 = assembly.split(',')
            opcode, operand1 = opcode_operand1.strip().split(' ')
            self.opcode = opcode.strip()
            self.op1 = operand1.strip()
            self.op2 = operand2.strip()
            self.op3 = operand3.strip()
        else:   # Single or no operand
            if assembly.count(' ') == 1:  # Single operand
                opcode, operand1 = assembly.split(' ')
                self.opcode, self.op1 = opcode.strip(), operand1.strip()
                self.type = INSTR_TYPE_BRANCH
            else:
                if "ret" in assembly:
                    self.opcode = "ret"
                    self.type = INSTR_TYPE_BRANCH
                else:
                    self.opcode = assembly

    def __str__(self):
        s = self.opcode
        if self.op1 is not None:
            s += " " + self.op1
            if self.op2 is not None:
                s += ", " + self.op2
                if self.op3 is not None:
                    s += ", " + self.op3
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
        self.end = len(self)
