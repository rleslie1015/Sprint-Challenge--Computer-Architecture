"""CPU functionality."""

import sys

"""
- [ ] Add the `CMP` instruction and `equal` flag to your LS-8.

- [ ] Add the `JMP` instruction.

- [ ] Add the `JEQ` and `JNE` instructions.
"""

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7

# bits to set for CMP IR
ltf = 0b100
gtf = 0b010
etf = 0b001

def DecimalToBinary(num): 
    if num > 1: 
        DecimalToBinary(num // 2) 
    # print(num % 2, end = '')
    return (num % 2)
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.reg[SP]  = 0xf4
        self.FL = 00000000
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[POP] = self.handle_pop
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[CMP] = self.handle_cmp

    def handle_cmp(self, operand_a, operand_b):
        # compare values
        if self.reg[operand_a] < self.reg[operand_b]:
            self.FL = ltf
        elif self.reg[operand_a] > self.reg[operand_b]:
            self.FL = gtf
        else:
            self.FL = etf
        # FL bits: 00000LGE
        # self.FL = DecimalToBinary(self.FL)
        # print('flag', self.FL)
     
    def push_val(self, value):
        # Decrement the stack pointer
        self.reg[SP] -= 1

        # Copy the value onto the stack
        top_of_stack_addr = self.reg[SP]
        self.ram[top_of_stack_addr] = value

    def pop_val(self):
        # Get value from top of stack
        top_of_stack_addr = self.reg[SP]
        value = self.ram[top_of_stack_addr] # Want to put this in a reg

        # Increment the SP
        self.reg[SP] += 1

        return value

    def handle_hlt(self, operand_a, operand_b):
        sys.exit()

    def handle_ldi(self, operand_a, operand_b):
        # operand_a = self.ram_read(self.pc + 1)
        # operand_b = self.ram_read(self.pc + 2)
        # print(operand_b)
        self.reg[operand_a] = operand_b

    def handle_prn(self, operand_a, operand_b):
        # reg_num = self.ram[self.pc+1]
        print(self.reg[operand_a])

    def handle_mul(self, num1, num2):
        # num1 = self.reg[0]
        # num2 = self.reg[1]
        product = num1 * num2
        operand_c = self.ram_read(self.pc+1)

        self.reg[operand_c] = product
    
    def handle_push(self, operand_a, operand_b):
        # decrement the stack pointer
        self.reg[SP] -= 1 

        # grab the value out of the given register
        reg_num = self.ram[self.pc+1]

        value = self.reg[reg_num] # the value we want to push

        # copy the value onto the stack
        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = value
    
    def handle_pop(self, operand_a, operand_b):
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
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(f'reg1 {operand_a}, reg2: {operand_b}')
            IR = self.ram[self.pc]
         
            if IR in self.branchtable:
                # find and run the intruction
                self.branchtable[IR](operand_a, operand_b)
                # set the pc depending on IR_len
                IR_len = (IR >> 6) + 1  
                self.pc += IR_len

            # The following may set the pc directly 
            elif IR == JMP:
                # set the pc to the address stored in the given register
                self.pc = self.reg[operand_a]

            elif IR == JEQ:
                # operand_a = self.ram[self.pc + 1]
                if self.FL & etf: # if the etf is true
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:
                if self.FL & etf == 0: # if etf is clear 
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2 
            else:
                raise Exception("IR not in branchtable or IR instruction not found")
            
           
