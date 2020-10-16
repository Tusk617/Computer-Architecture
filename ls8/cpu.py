"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.sp = 7
        self.fl = 0b00000000
    
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                #can be interpreted as "for instruction in program"
                for line in f:
                    line = line.strip()

                    #accounting for any comments or blank lines
                    if line == '' or line[0] == '#':
                        continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)

                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit()
                    
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"File not found!: {sys.argv[1]}")
            sys.exit(0)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def push_v(self, value):
        #decrement SP
        self.register[self.sp] -= 1

        #copy value onto stack
        top_stack = self.register[self.sp]
        value = self.ram[top_stack]
    
    def pop_v(self):

        top_stack = self.register[self.sp]
        value = self.ram[top_stack]

        self.register[self.sp] += 1

        return value
    def run(self):
        """Run the CPU."""
        self.trace()
        self.register[self.sp] == 0xf4
        
        running = True

        while running is True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                #HLT
                self.pc += 1
                running = False
            elif ir == LDI:
                #LDI
                reg_num = operand_a
                value = operand_b
                self.register[reg_num] = value
                self.pc += 3
            elif ir == PRN:
                #PRN
                reg_num = operand_a
                print(self.register[reg_num])
                self.pc += 2
            elif ir == MUL:
                regA = operand_a
                regB = operand_b
                self.register[regA] = self.register[regA] * self.register[regB]
                self.pc += 3
            elif ir == ADD:
                regA = operand_a
                regB = operand_b
                self.register[regA] = self.register[regA] + self.register[regB]
                self.pc += 3
            elif ir == PUSH:
                #Decrement the `SP`.
                self.register[self.sp] -= 1
                #grab the value out of that given register
                reg_num = operand_a
                value = self.register[reg_num]

                #copy value into register
                self.ram[self.register[self.sp]] = value

                self.pc += 2
            elif ir == POP:
                #value is top of stack address
                value = self.ram[self.register[self.sp]]

                # reg_num = operand_a
                self.register[operand_a] = value

                self.register[self.sp] += 1

                self.pc += 2
            elif ir == CALL:

                returnAddy = self.pc + 2

                self.push_v(returnAddy)

                reg_num = self.ram[self.pc + 1]
                subAddy = self.register[reg_num]

                self.pc = subAddy
            elif ir == RET:
                returnAddy = self.pop_v()

                self.pc = returnAddy
            elif ir == CMP:
                #need to update current flag status based on reg comparison
                #first create the two registers to be compared
                regA = operand_a
                regB = operand_b
                #next compare the values
                #less than
                if self.register[regA] < self.register[regB]:
                    self.fl = 0b00000100
                #greater than
                elif self.register[regA] > self.register[regB]:
                    self.fl = 0b00000010
                #equal to
                elif self.register[regA] == self.register[regB]:
                    self.fl = 0b00000001
            else:
                print("Unkown command!")
                sys.exit(0)

