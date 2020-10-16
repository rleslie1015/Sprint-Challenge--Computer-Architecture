"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.reg[SP]  = 0xf4
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[POP] = self.handle_pop
        self.branchtable[PUSH] = self.handle_push
    
    def handle_hlt(self):
        sys.exit()

    def handle_ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b

    def handle_prn(self):
        reg_num = self.ram[self.pc+1]
        print(self.reg[reg_num])

    def handle_mul(self):
        num1 = self.reg[0]
        num2 = self.reg[1]
        product = num1 * num2
        operand_c = self.ram_read(self.pc+1)

        self.reg[operand_c] = product
    
    def handle_push(self):
        # decrement the stack pointer
        self.reg[SP] -= 1 

        # grab the value out of the given register
        reg_num = self.ram[self.pc+1]

        value = self.reg[reg_num] # the value we want to push

        # copy the value onto the stack
        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = value
    
    def handle_pop(self):
        # get value from top of stack
        top_of_stack_addr = self.reg[SP]
        value = self.ram[top_of_stack_addr] # value we want to put in reg

        # store in the register
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value
        # print(memory[0xf0:0xf4])

        self.reg[SP] += 1

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: compy.py progname")
            sys.exit(1)
        # try to open the file from second arg     
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    # print(line)
                    if line == '' or line[0] == "#":
                        continue
                    # reading instructions line by line
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2) # casting into inter with base of 2 (binary)
                    
                    except ValueError: 
                        print(f"Invalid number {str_value}")
                        sys.exit(1)
                    
                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)
        # For now, we've just hardcoded a program:
        # print(self.ram[:50])
        # sys.exit()
        # program = [
        #     # From print8.ls8
          
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        # print('address', address)
        # print('value', value)
        self.ram[address] = value

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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        while not self.running:
            # self.trace()
            instruction = self.ram[self.pc]
         
            self.branchtable[instruction]() 

            instruction_len = (instruction >> 6) + 1
            # print('instruction len', instruction_len)
            self.pc += instruction_len
