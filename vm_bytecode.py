#!/usr/bin/env python3
"""Stack-based virtual machine with bytecode."""
import struct
OP_PUSH,OP_POP,OP_ADD,OP_SUB,OP_MUL,OP_DIV,OP_MOD=range(7)
OP_EQ,OP_LT,OP_GT,OP_AND,OP_OR,OP_NOT=range(7,13)
OP_JMP,OP_JZ,OP_JNZ=range(13,16)
OP_LOAD,OP_STORE,OP_CALL,OP_RET,OP_PRINT,OP_HALT=range(16,22)
OP_DUP,OP_SWAP,OP_ROT=range(22,25)
class VM:
    def __init__(self,code,data=None):
        self.code=code;self.stack=[];self.frames=[];self.ip=0;self.vars={}
        self.data=data or [];self.running=True;self.output=[]
    def run(self,max_steps=100000):
        for _ in range(max_steps):
            if not self.running or self.ip>=len(self.code): break
            self.step()
        return self.output
    def step(self):
        op=self.code[self.ip];self.ip+=1
        if op==OP_PUSH: self.stack.append(self.code[self.ip]);self.ip+=1
        elif op==OP_POP: self.stack.pop()
        elif op==OP_ADD: b,a=self.stack.pop(),self.stack.pop();self.stack.append(a+b)
        elif op==OP_SUB: b,a=self.stack.pop(),self.stack.pop();self.stack.append(a-b)
        elif op==OP_MUL: b,a=self.stack.pop(),self.stack.pop();self.stack.append(a*b)
        elif op==OP_DIV: b,a=self.stack.pop(),self.stack.pop();self.stack.append(a//b)
        elif op==OP_MOD: b,a=self.stack.pop(),self.stack.pop();self.stack.append(a%b)
        elif op==OP_EQ: b,a=self.stack.pop(),self.stack.pop();self.stack.append(int(a==b))
        elif op==OP_LT: b,a=self.stack.pop(),self.stack.pop();self.stack.append(int(a<b))
        elif op==OP_GT: b,a=self.stack.pop(),self.stack.pop();self.stack.append(int(a>b))
        elif op==OP_NOT: self.stack.append(int(not self.stack.pop()))
        elif op==OP_JMP: self.ip=self.code[self.ip]
        elif op==OP_JZ: addr=self.code[self.ip];self.ip+=1;
        elif op==OP_JNZ: addr=self.code[self.ip];self.ip+=1;
        elif op==OP_LOAD: self.stack.append(self.vars.get(self.code[self.ip],0));self.ip+=1
        elif op==OP_STORE: self.vars[self.code[self.ip]]=self.stack.pop();self.ip+=1
        elif op==OP_CALL: self.frames.append(self.ip+1);self.ip=self.code[self.ip]
        elif op==OP_RET: self.ip=self.frames.pop()
        elif op==OP_PRINT: self.output.append(self.stack.pop())
        elif op==OP_HALT: self.running=False
        elif op==OP_DUP: self.stack.append(self.stack[-1])
        elif op==OP_SWAP: self.stack[-1],self.stack[-2]=self.stack[-2],self.stack[-1]
        if op==OP_JZ: 
            if not self.stack.pop(): self.ip=addr
        elif op==OP_JNZ:
            if self.stack.pop(): self.ip=addr
if __name__=="__main__":
    # Compute 10! iteratively
    code=[OP_PUSH,1,OP_STORE,0,OP_PUSH,10,OP_STORE,1,  # result=1, n=10
        OP_LOAD,1,OP_PUSH,1,OP_GT,OP_JZ,32,  # while n>1
        OP_LOAD,0,OP_LOAD,1,OP_MUL,OP_STORE,0,  # result*=n
        OP_LOAD,1,OP_PUSH,1,OP_SUB,OP_STORE,1,  # n-=1
        OP_JMP,8,  # loop
        OP_LOAD,0,OP_PRINT,OP_HALT]
    vm=VM(code);out=vm.run()
    assert out==[3628800];print(f"10! = {out[0]}")
    print("VM bytecode OK")
