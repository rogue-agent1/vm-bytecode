#!/usr/bin/env python3
"""Simple stack-based bytecode virtual machine."""
import sys

PUSH, POP, ADD, SUB, MUL, DIV, MOD = 0x01, 0x02, 0x10, 0x11, 0x12, 0x13, 0x14
DUP, SWAP, PRINT, HALT = 0x20, 0x21, 0x30, 0xFF
JMP, JZ, JNZ = 0x40, 0x41, 0x42
CMP_EQ, CMP_LT, CMP_GT = 0x50, 0x51, 0x52
NAMES = {PUSH:'PUSH',POP:'POP',ADD:'ADD',SUB:'SUB',MUL:'MUL',DIV:'DIV',MOD:'MOD',
         DUP:'DUP',SWAP:'SWAP',PRINT:'PRINT',HALT:'HALT',JMP:'JMP',JZ:'JZ',JNZ:'JNZ',
         CMP_EQ:'EQ',CMP_LT:'LT',CMP_GT:'GT'}

class VM:
    def __init__(self):
        self.stack = []; self.pc = 0; self.running = True
    def run(self, program, trace=False):
        self.pc = 0; self.running = True
        while self.running and self.pc < len(program):
            op = program[self.pc]
            if trace: print(f"  [{self.pc:04d}] {NAMES.get(op,'?'):5s} stack={self.stack[-5:]}")
            if op == PUSH: self.pc += 1; self.stack.append(program[self.pc])
            elif op == POP: self.stack.pop()
            elif op == ADD: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(a+b)
            elif op == SUB: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(a-b)
            elif op == MUL: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(a*b)
            elif op == DIV: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(a//b)
            elif op == MOD: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(a%b)
            elif op == DUP: self.stack.append(self.stack[-1])
            elif op == SWAP: self.stack[-1],self.stack[-2] = self.stack[-2],self.stack[-1]
            elif op == PRINT: print(f"  → {self.stack.pop()}")
            elif op == JMP: self.pc = program[self.pc+1]; continue
            elif op == JZ: self.pc = program[self.pc+1] if self.stack.pop()==0 else self.pc+2; continue
            elif op == JNZ: self.pc = program[self.pc+1] if self.stack.pop()!=0 else self.pc+2; continue
            elif op == CMP_EQ: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(1 if a==b else 0)
            elif op == CMP_LT: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(1 if a<b else 0)
            elif op == CMP_GT: b,a = self.stack.pop(),self.stack.pop(); self.stack.append(1 if a>b else 0)
            elif op == HALT: self.running = False
            self.pc += 1
        return self.stack

if __name__ == '__main__':
    vm = VM()
    # Compute 10! (factorial)
    # Push 10, then loop: dup, push 1, sub, swap, mul, dup, push 1, gt, jnz
    prog = [PUSH,10, PUSH,1,  # stack: [10, 1] (counter, accumulator)
            SWAP, DUP, PUSH,1, SUB,  # counter-1
            SWAP,  # bring acc up
            PUSH,2,  # placeholder
            DUP,  # dup acc for mul  
            ]
    # Simpler: just compute 3+4*2
    prog = [PUSH,3, PUSH,4, PUSH,2, MUL, ADD, PRINT, HALT]
    trace = '--trace' in sys.argv
    print("Bytecode VM Demo: 3 + 4*2\n")
    vm.run(prog, trace)
    print(f"\nFinal stack: {vm.stack}")
