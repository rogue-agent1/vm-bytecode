#!/usr/bin/env python3
"""Stack-based bytecode VM."""
import sys
OP_PUSH,OP_POP,OP_ADD,OP_SUB,OP_MUL,OP_DIV,OP_MOD=range(7)
OP_DUP,OP_SWAP,OP_PRINT,OP_HALT=range(7,11)
OP_JMP,OP_JZ,OP_JNZ,OP_EQ,OP_LT,OP_GT=range(11,17)
OP_LOAD,OP_STORE,OP_CALL,OP_RET=range(17,21)
NAMES={v:k[3:] for k,v in globals().items() if k.startswith('OP_')}
class VM:
    def __init__(self,code):
        self.code=code; self.stack=[]; self.ip=0
        self.locals=[0]*256; self.callstack=[]; self.output=[]
    def run(self):
        while self.ip<len(self.code):
            op=self.code[self.ip]; self.ip+=1
            if op==OP_PUSH: self.stack.append(self.code[self.ip]); self.ip+=1
            elif op==OP_POP: self.stack.pop()
            elif op==OP_ADD: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a+b)
            elif op==OP_SUB: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a-b)
            elif op==OP_MUL: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a*b)
            elif op==OP_DIV: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a//b)
            elif op==OP_MOD: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(a%b)
            elif op==OP_DUP: self.stack.append(self.stack[-1])
            elif op==OP_SWAP: self.stack[-1],self.stack[-2]=self.stack[-2],self.stack[-1]
            elif op==OP_PRINT: self.output.append(str(self.stack.pop()))
            elif op==OP_HALT: break
            elif op==OP_JMP: self.ip=self.code[self.ip]
            elif op==OP_JZ: addr=self.code[self.ip]; self.ip=addr if self.stack.pop()==0 else self.ip+1
            elif op==OP_JNZ: addr=self.code[self.ip]; self.ip=addr if self.stack.pop()!=0 else self.ip+1
            elif op==OP_EQ: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(1 if a==b else 0)
            elif op==OP_LT: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(1 if a<b else 0)
            elif op==OP_GT: b,a=self.stack.pop(),self.stack.pop(); self.stack.append(1 if a>b else 0)
            elif op==OP_LOAD: self.stack.append(self.locals[self.code[self.ip]]); self.ip+=1
            elif op==OP_STORE: self.locals[self.code[self.ip]]=self.stack.pop(); self.ip+=1
            elif op==OP_CALL: self.callstack.append(self.ip+1); self.ip=self.code[self.ip]
            elif op==OP_RET: self.ip=self.callstack.pop()
        return self.output
def main():
    # Compute 1+2+...+10
    code=[
        OP_PUSH,0,OP_STORE,0,   # sum=0
        OP_PUSH,1,OP_STORE,1,   # i=1
        # loop (ip=8):
        OP_LOAD,1,OP_PUSH,11,OP_LT,  # i<11?
        OP_JZ,30,                # if not, jump to end
        OP_LOAD,0,OP_LOAD,1,OP_ADD,OP_STORE,0,  # sum+=i
        OP_LOAD,1,OP_PUSH,1,OP_ADD,OP_STORE,1,  # i++
        OP_JMP,8,                # loop
        # end (ip=30):
        OP_LOAD,0,OP_PRINT,OP_HALT
    ]
    vm=VM(code); out=vm.run()
    print(f"Sum 1..10 = {out[0]}")
    # Factorial 5
    code2=[
        OP_PUSH,5,OP_STORE,0,  # n=5
        OP_PUSH,1,OP_STORE,1,  # result=1
        # loop (ip=8):
        OP_LOAD,0,OP_PUSH,0,OP_GT,
        OP_JZ,26,
        OP_LOAD,1,OP_LOAD,0,OP_MUL,OP_STORE,1,
        OP_LOAD,0,OP_PUSH,1,OP_SUB,OP_STORE,0,
        OP_JMP,8,
        # end (ip=26):
        OP_LOAD,1,OP_PRINT,OP_HALT
    ]
    vm2=VM(code2); out2=vm2.run()
    print(f"5! = {out2[0]}")
if __name__=="__main__": main()
