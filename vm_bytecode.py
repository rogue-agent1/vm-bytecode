#!/usr/bin/env python3
"""Stack-based bytecode virtual machine."""
import sys, struct

# Opcodes
PUSH, POP, DUP, SWAP = 0x01, 0x02, 0x03, 0x04
ADD, SUB, MUL, DIV, MOD = 0x10, 0x11, 0x12, 0x13, 0x14
AND, OR, XOR, NOT, SHL, SHR = 0x20, 0x21, 0x22, 0x23, 0x24, 0x25
EQ, NE, LT, GT = 0x30, 0x31, 0x32, 0x33
JMP, JZ, JNZ, CALL, RET = 0x40, 0x41, 0x42, 0x43, 0x44
LOAD, STORE = 0x50, 0x51
PRINT, HALT = 0xF0, 0xFF

OP_NAMES = {v: k for k, v in {**locals()}.items() if isinstance(v, int) and 0 < v < 0x100}

class VM:
    def __init__(self, mem_size=4096):
        self.stack = []; self.call_stack = []
        self.mem = [0] * mem_size; self.pc = 0
        self.output = []; self.halted = False

    def run(self, bytecode, max_steps=100000):
        code = bytecode
        for _ in range(max_steps):
            if self.pc >= len(code) or self.halted: break
            op = code[self.pc]; self.pc += 1
            if op == PUSH:
                val = struct.unpack_from(">i", bytes(code[self.pc:self.pc+4]))[0]
                self.stack.append(val); self.pc += 4
            elif op == POP: self.stack.pop()
            elif op == DUP: self.stack.append(self.stack[-1])
            elif op == SWAP: self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            elif op == ADD: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a + b)
            elif op == SUB: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a - b)
            elif op == MUL: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a * b)
            elif op == DIV: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a // b if b else 0)
            elif op == MOD: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a % b if b else 0)
            elif op == AND: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a & b)
            elif op == OR: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a | b)
            elif op == XOR: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a ^ b)
            elif op == NOT: self.stack.append(~self.stack.pop())
            elif op == EQ: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(int(a == b))
            elif op == NE: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(int(a != b))
            elif op == LT: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(int(a < b))
            elif op == GT: b, a = self.stack.pop(), self.stack.pop(); self.stack.append(int(a > b))
            elif op == JMP:
                addr = struct.unpack_from(">H", bytes(code[self.pc:self.pc+2]))[0]
                self.pc = addr
            elif op == JZ:
                addr = struct.unpack_from(">H", bytes(code[self.pc:self.pc+2]))[0]
                self.pc = addr if self.stack.pop() == 0 else self.pc + 2
            elif op == JNZ:
                addr = struct.unpack_from(">H", bytes(code[self.pc:self.pc+2]))[0]
                self.pc = addr if self.stack.pop() != 0 else self.pc + 2
            elif op == CALL:
                addr = struct.unpack_from(">H", bytes(code[self.pc:self.pc+2]))[0]
                self.call_stack.append(self.pc + 2); self.pc = addr
            elif op == RET: self.pc = self.call_stack.pop()
            elif op == LOAD: self.stack.append(self.mem[self.stack.pop()])
            elif op == STORE:
                addr, val = self.stack.pop(), self.stack.pop()
                self.mem[addr] = val
            elif op == PRINT: self.output.append(self.stack.pop())
            elif op == HALT: self.halted = True

def assemble(text):
    """Simple assembler: PUSH 42, ADD, PRINT, HALT etc."""
    code = []
    for line in text.strip().split("\n"):
        line = line.split(";")[0].strip()
        if not line: continue
        parts = line.split()
        name = parts[0].upper()
        op = {v: k for k, v in OP_NAMES.items()}.get(name)
        if op is None: continue
        code.append(op)
        if op == PUSH:
            val = int(parts[1])
            code.extend(struct.pack(">i", val))
        elif op in (JMP, JZ, JNZ, CALL):
            addr = int(parts[1])
            code.extend(struct.pack(">H", addr))
    return code

def main():
    if len(sys.argv) < 2:
        print("Usage: vm_bytecode.py <file.asm>")
        print("Demo: computing 3 + 4 * 5")
        code = assemble("PUSH 4\nPUSH 5\nMUL\nPUSH 3\nADD\nPRINT\nHALT")
        vm = VM(); vm.run(code)
        print(f"Output: {vm.output}"); return
    with open(sys.argv[1]) as f: text = f.read()
    code = assemble(text)
    vm = VM(); vm.run(code)
    for v in vm.output: print(v)

if __name__ == "__main__": main()
