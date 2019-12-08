import re

INSTR_TYPE_ALU = 1    # Logical and arith operations
INSTR_TYPE_MEM = 2      # Load and stores
INSTR_TYPE_BRANCH = 4   # Branches


class Instruction:
    def __init__(self, assembly):
        self.opcode = None
        self.op1 = None
        self.op2 = None
        self.op3 = None
        self.reg_operands = []      # Contains a list of non-None operands excluding immediate values
        self.type = None
        self.parse(assembly)

    def parse(self, assembly):
        """
        Set the members of the class to the given instruction
        :type assembly: str
        :return: None
        """
        if assembly[0] == '#' or assembly == '\n':  # Start with a comment or empty line, so insert WAIT
            self.opcode = "nop"
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

            # First operand should always be a register, don't check that
            if self.__check_operand_matches_reg(self.op2):
                self.reg_operands = [self.op1, self.op2]
            else:
                self.reg_operands = [self.op1]
        elif comma_count == 2:  # 3 operands
            opcode_operand1, operand2, operand3 = assembly.split(',')
            opcode, operand1 = opcode_operand1.strip().split(' ')
            self.opcode = opcode.strip()
            self.op1 = operand1.strip()
            self.op2 = operand2.strip()
            self.op3 = operand3.strip()

            # First and second operand should always be registers, don't check them
            if self.__check_operand_matches_reg(self.op3):
                self.reg_operands = [self.op1, self.op2, self.op3]
            else:
                self.reg_operands = [self.op1, self.op2]

        else:   # Single or no operand
            if assembly.count(' ') == 1:  # Single operand
                opcode, operand1 = assembly.split(' ')
                self.opcode, self.op1 = opcode.strip(), operand1.strip()
            else:
                if "ret" in assembly:
                    self.opcode = "ret"
                else:
                    self.opcode = assembly
            # There is no single-operand instructions taking a register as operand
            self.reg_operands = []  # Useless because default value.

        if self.opcode in ["ldr", "str", "push", "pop"]:
            self.type = INSTR_TYPE_MEM
        elif self.opcode in ["b", "br", "ret", "be", "bg"]:
            self.type = INSTR_TYPE_BRANCH
        else:
            self.type = INSTR_TYPE_ALU

    def __check_operand_matches_reg(self, operand):
        """
        Checks that the given string is a register operand
        """
        return re.search("r[0-31]", operand) is not None

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
            if line not in ["", "#" "\n"]:
                self.append(Instruction(line))
            else:
                self.append(None)
        file.close()
        self.end = len(self)
