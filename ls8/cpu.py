"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    opcodes = {"HLT": 0b00000001,    # 1
               "LDI": 0b10000010,    # 130
               "PRN": 0b01000111,    # 71
               "MUL": 0b10100010,    # 162
               "PUSH": 0b01000101,   # 69
               "POP": 0b01000110,    # 70
               "ADD": 0b10100000,  # 160
               "SUB": 0b10100001,  # 161
               "MUL": 0b10100010,  # 162
               "DIV": 0b10100011,  # 163
               "MOD": 0b10100100,  # 164
               "INC": 0b01100101,  # 101
               "DEC": 0b01100110,  # 102
               "CMP": 0b10100111,  # 167
               "AND": 0b10101000,  # 168
               "NOT": 0b01101001,  # 105
               "OR ": 0b10101010,  # 170
               "XOR": 0b10101011,  # 171
               "SHL": 0b10101100,  # 172
               "SHR": 0b10101101, }  # 173

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
        self.ram = [0]*256  # available system ram
        self.fl = [0]*8  # Flags
        # Program Counter, address of the currently executing instruction
        self.pc = 0
        self.register = [0, 0, 0, 0, 0, 0, 0, 0xf4]  # 8-bit register
        self.branch_table = {self.opcodes["HLT"]: self.hlt,
                             self.opcodes["LDI"]: self.ldi,
                             self.opcodes["PRN"]: self.prn,
                             self.opcodes["MUL"]: self.mul, }
        # self.opcodes["POP"]: self.pop,
        # self.opcodes["PUSH"]: self.push}
        self.running = True

    def load(self, filename):
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
        address = 0
        try:
            #            filename = sys.argv[1]
            with open(filename) as f:
                for line in f:
                    # split lines into opcodes and other cruft
                    line = line.split("#")[0].strip()
                    # print(address, line)
                    if line == "":  # if no opcode is present
                        continue
                    else:  # add opcode to memory
                        v = int(line, 2)
                        # print(address, v)
                        self.ram[address] = v
                        address += 1
        # handle user not supplying correct data
        except (IndexError, FileNotFoundError):
            print("Please provide a valid filename!")
            exit(1)

        # filename = sys.argv[1]
        # with open(filename) as f:
        #     for address, line in enumerate(f):
        #         print(address, line)
        #         line = line.split("#")
        #         try:
        #             v = int(line[0], 2)
        #         except FileNotFoundError:
        #             print("Please provide a valid filename!")
        #         except ValueError:
        #             continue
        #         self.ram[address] = v

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
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

    def hlt(self):
        ''' system halt '''
        self.running = False

    def ldi(self):
        ''' load a value into a register '''
        self.register[self.ram[self.pc+1]] = self.ram[self.pc+2]
        # print(f'''
        #       self.pc {self.pc}
        #       self.ram[self.pc] {self.ram[self.pc]}
        #       self.register[self.ram[self.pc+1]] {self.register[self.ram[self.pc+1]]}
        #       self.ram[self.pc] bitshift {(self.ram[self.pc] & 0b11000000 >> 6)+1}''')
#        self.pc += (self.ram[self.pc] & 0b11000000 >> 6) + 1
        self.pc += 3

    def prn(self):
        ''' print value of a register '''
        print(self.register[self.ram[self.pc+1]])
#        self.pc += (self.ram[self.pc] & 0b11000000 >> 6) + 1
        self.pc += 2

    def mul(self):
        ''' multiply to register values '''
        self.register[self.ram[self.pc+1]] = self.register[self.ram[self.pc+2]
                                                           ]*self.register[self.ram[self.pc+1]]
#        self.pc += (self.ram[self.pc] & 0b11000000 >> 6) + 1
        self.pc += 3

    def call_function(self, function):
        ''' branch table call functionality '''
        try:
            self.branch_table[function]()
        except KeyError:
            print(f"This operation ({bin(function)}) not yet implemented!")
            exit(1)
        # if self.branch_table[function] is not None:
        #     self.branch_table[function]()
        # else:
        #     print("This operation not yet implemented!")
        #     exit(1)

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram_read(self.pc)
            self.call_function(ir)
        # running = True
        # while running:
        #     ir = self.ram_read(self.pc)
        #     # print(ir)
        #     # command = self.ram_read(self.pc)
        #     # print(bin(command))
        #     # operand_A = self.ram_read(self.pc + 1)
        #     # operand_B = self.ram_read(self.pc + 2)
        #     # print("ir is ", ir)
        #     # print(self.commands["HLT"])
        #     # print(self.commands["LDI"])
        #     # print(self.commands["PRN"])
        #     # print(self.ram[self.commands["HLT"]])
        #     # print(self.ram[self.commands["LDI"]])
        #     # print(self.ram[self.commands["PRN"]])
        #     # print(self.R0[self.commands["HLT"]])
        #     # print(self.R0[self.commands["LDI"]])
        #     # print(self.R0[self.commands["PRN"]])
        #     if ir == self.opcodes["HLT"]:
        #         running = False
        #         self.pc += 1
        #     elif ir == self.opcodes["LDI"]:
        #         self.register[self.ram[self.pc+1]] = self.ram[self.pc+2]
        #         self.pc += 3
        #     elif ir == self.opcodes["PRN"]:
        #         print(self.register[self.ram[self.pc+1]])
        #         self.pc += 2
        #     elif ir == self.opcodes["MUL"]:
        #         self.register[self.ram[self.pc+1]
        #                       ] = self.register[self.ram[self.pc+2]]*self.register[self.ram[self.pc+1]]
        #         self.pc += 3
        #     else:
        #         print(f'Unknown instruction {ir} at address {self.pc}')
        #         sys.exit(1)

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
