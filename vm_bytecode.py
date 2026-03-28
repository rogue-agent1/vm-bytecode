#!/usr/bin/env python3
"""Stack VM — bytecode interpreter with arithmetic and control flow."""
import sys
PUSH,POP,ADD,SUB,MUL,DIV,DUP,SWAP,PRINT,HALT=range(10)
JMP,JZ,JNZ,CMP,LOAD,STORE=10,11,12,13,14,15
OP_NAMES={PUSH:"PUSH",POP:"POP",ADD:"ADD",SUB:"SUB",MUL:"MUL",DIV:"DIV",DUP:"DUP",SWAP:"SWAP",PRINT:"PRINT",HALT:"HALT",JMP:"JMP",JZ:"JZ",JNZ:"JNZ",CMP:"CMP",LOAD:"LOAD",STORE:"STORE"}
class VM:
    def __init__(self): self.stack=[]; self.memory={}; self.ip=0
    def run(self, program, trace=False):
        self.ip=0
        while self.ip<len(program):
            op=program[self.ip]
            if trace: print(f"  [{self.ip:>3}] {OP_NAMES.get(op,'?'):>6} stack={self.stack[:5]}")
            if op==PUSH: self.ip+=1; self.stack.append(program[self.ip])
            elif op==POP: self.stack.pop()
            elif op==ADD: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a+b)
            elif op==SUB: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a-b)
            elif op==MUL: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a*b)
            elif op==DIV: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a//b)
            elif op==DUP: self.stack.append(self.stack[-1])
            elif op==SWAP: self.stack[-1],self.stack[-2]=self.stack[-2],self.stack[-1]
            elif op==PRINT: print(f"  OUT: {self.stack.pop()}")
            elif op==HALT: return
            elif op==JMP: self.ip=program[self.ip+1]; continue
            elif op==JZ: self.ip=(program[self.ip+1] if self.stack.pop()==0 else self.ip+2); continue
            elif op==STORE: self.ip+=1; self.memory[program[self.ip]]=self.stack.pop()
            elif op==LOAD: self.ip+=1; self.stack.append(self.memory.get(program[self.ip],0))
            self.ip+=1
def cli():
    vm=VM()
    # Compute 10! iteratively
    prog=[PUSH,1,STORE,0,PUSH,10,STORE,1,  # result=1, n=10
          LOAD,1,PUSH,0,CMP,JZ,28,         # while n>0
          LOAD,0,LOAD,1,MUL,STORE,0,       # result*=n
          LOAD,1,PUSH,1,SUB,STORE,1,       # n-=1
          JMP,8,                             # loop
          LOAD,0,PRINT,HALT]                # print result
    print("  Computing 10!:")
    # Simpler: just 5*3+2
    prog2=[PUSH,5,PUSH,3,MUL,PUSH,2,ADD,PRINT,HALT]
    vm.run(prog2, trace="--trace" in sys.argv)
if __name__=="__main__": cli()
