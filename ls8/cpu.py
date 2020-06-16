"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    opcodes = {"HLT": 0b00000001,  # 1
               "LDI": 0b10000010,  # 130
               "PRN": 0b01000111}  # 71

    def __init__(self):
        """Construct a new CPU."""
        # self.R0 = [0]*8
        # self.R1 = [0]*8
        # self.R2 = [0]*8
        # self.R3 = [0]*8
        # self.R4 = [0]*8
        # self.R5 = [0]*8  # reserved as the interrupt mask (IM)
        # self.R6 = [0]*8  # reserved as the interrupt status (IS)
        # self.R7 = [0]*8  # reserved as the stack pointer (SP)
        self.ram = [0]*256
        self.fl = [0]*8  # Flags
        # Program Counter, address of the currently executing instruction
        self.pc = 0
        self.register = [0]*8  # 8-bit register

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        filename = sys.argv[1]

        with open(filename) as f:
            for address, line in enumerate(f):
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram[address] = v

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        ''' accept the address to read and return the value stored there
        input: Memory Address Register (MAR)
        output: Memory Data Register (MDR)'''
        try:
            return self.ram[MAR]
        except IndexError:
            raise ValueError(f"The address {MAR} isn't valid.")

    def ram_write(self, MAR, MDR):
        ''' accept a value to write, and the address to write it to
        input: Memory Address Register (MAR)
               Memory Data Register (MDR) '''
        try:
            self.ram[MAR] = MDR
        except IndexError:
            raise ValueError(f"The address {MAR} isn't valid.")

    def run(self):
        """Run the CPU."""
        running = True
        # ir = self.ram[self.pc]
        # print(ir)
        while running:
            ir = self.ram_read(self.pc)
#            print(ir)
            # command = self.ram_read(self.pc)
            # print(bin(command))
            # operand_A = self.ram_read(self.pc + 1)
            # operand_B = self.ram_read(self.pc + 2)
            # print("ir is ", ir)
            # print(self.commands["HLT"])
            # print(self.commands["LDI"])
            # print(self.commands["PRN"])
            # print(self.ram[self.commands["HLT"]])
            # print(self.ram[self.commands["LDI"]])
            # print(self.ram[self.commands["PRN"]])
            # print(self.R0[self.commands["HLT"]])
            # print(self.R0[self.commands["LDI"]])
            # print(self.R0[self.commands["PRN"]])
            if ir == self.opcodes["HLT"]:
                running = False
                self.pc += 1
            elif ir == self.opcodes["LDI"]:
                self.register[self.ram[self.pc+1]] = self.ram[self.pc+2]
                self.pc += 3
            elif ir == self.opcodes["PRN"]:
                print(self.register[self.ram[self.pc+1]])
                self.pc += 2
            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)

# if __name__ == "__main__":
#     filename = sys.argv[1]

#     with open(filename) as f:
#         for address, line in enumerate(f):
#             line = line.split("#")
#             try:
#                 v = int(line[0], 10)
#             except ValueError:
#                 continue
#             memory[address] = v
