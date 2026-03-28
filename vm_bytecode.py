#!/usr/bin/env python3
"""vm_bytecode - Stack-based bytecode virtual machine."""
import sys
PUSH,POP,ADD,SUB,MUL,DIV,MOD,DUP,SWAP,OVER=range(10)
EQ,LT,GT,NOT,AND,OR,JMP,JZ,JNZ,CALL=range(10,20)
RET,LOAD,STORE,PRINT,HALT=range(20,25)
NAMES={PUSH:"PUSH",POP:"POP",ADD:"ADD",SUB:"SUB",MUL:"MUL",DIV:"DIV",MOD:"MOD",DUP:"DUP",SWAP:"SWAP",OVER:"OVER",
    EQ:"EQ",LT:"LT",GT:"GT",NOT:"NOT",AND:"AND",OR:"OR",JMP:"JMP",JZ:"JZ",JNZ:"JNZ",CALL:"CALL",
    RET:"RET",LOAD:"LOAD",STORE:"STORE",PRINT:"PRINT",HALT:"HALT"}
class VM:
    def __init__(s):s.stack=[];s.memory={};s.call_stack=[];s.ip=0
    def run(s,program):
        s.ip=0
        while s.ip<len(program):
            op=program[s.ip];s.ip+=1
            if op==PUSH:s.stack.append(program[s.ip]);s.ip+=1
            elif op==POP:s.stack.pop()
            elif op==ADD:b,a=s.stack.pop(),s.stack.pop();s.stack.append(a+b)
            elif op==SUB:b,a=s.stack.pop(),s.stack.pop();s.stack.append(a-b)
            elif op==MUL:b,a=s.stack.pop(),s.stack.pop();s.stack.append(a*b)
            elif op==DIV:b,a=s.stack.pop(),s.stack.pop();s.stack.append(a//b)
            elif op==MOD:b,a=s.stack.pop(),s.stack.pop();s.stack.append(a%b)
            elif op==DUP:s.stack.append(s.stack[-1])
            elif op==SWAP:s.stack[-1],s.stack[-2]=s.stack[-2],s.stack[-1]
            elif op==EQ:b,a=s.stack.pop(),s.stack.pop();s.stack.append(int(a==b))
            elif op==LT:b,a=s.stack.pop(),s.stack.pop();s.stack.append(int(a<b))
            elif op==GT:b,a=s.stack.pop(),s.stack.pop();s.stack.append(int(a>b))
            elif op==JMP:s.ip=program[s.ip]
            elif op==JZ:addr=program[s.ip];s.ip+=1;
            if not s.stack.pop():s.ip=addr
            elif op==JNZ:addr=program[s.ip];s.ip+=1;
            if s.stack.pop():s.ip=addr
            elif op==CALL:s.call_stack.append(s.ip+1);s.ip=program[s.ip]
            elif op==RET:s.ip=s.call_stack.pop()
            elif op==LOAD:s.stack.append(s.memory.get(program[s.ip],0));s.ip+=1
            elif op==STORE:s.memory[program[s.ip]]=s.stack.pop();s.ip+=1
            elif op==PRINT:print(f"  > {s.stack.pop()}")
            elif op==HALT:return
        return s.stack
if __name__=="__main__":
    vm=VM()
    # Compute factorial of 5
    prog=[PUSH,5,PUSH,1,SWAP,DUP,PUSH,1,EQ,JNZ,18,SWAP,OVER,MUL,SWAP,PUSH,1,SUB,JMP,4,POP,PRINT,HALT]
    print("Factorial of 5:");vm.run(prog)
