# Project 7 & 8: Virtual Machine (of Hack language)
The VMTranslator.py takes a collection of .vm files as input and produces a single Hack assembly language .asm file as output

More info:  
* https://www.nand2tetris.org/project07
* https://www.nand2tetris.org/project08

### Launch example:
```
python VMTranslator.py [file.vm] // if VM program consists of one file
python VMTranslator.py [local_directory] // where local_directory is the name of directory containing .vm files

```

### Example of input program with extension .vm:
```
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm

// Performs a simple calculation and returns the result.
function SimpleFunction.test 2
push local 0
push local 1
add
not
push argument 0
add
push argument 1
sub
return
```

### Output example (file with extension .asm):
```
(SimpleFunction.test)
@2
D=A
@n_locals
M=D
@0
D=A
@i
M=D
(INITLOOPSimpleFunction.test)
@i
M=M+1
D=M
@n_locals
D=M-D
@ENDINITSimpleFunction.test
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@INITLOOPSimpleFunction.test
0;JMP
(ENDINITSimpleFunction.test)
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
@SP
A=M-1
M=!M
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@LCL
D=M
@endFrame
MD=D
@5
A=D-A
D=M
@retAddr
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@endFrame
M=M-1
A=M
D=M
@THAT
M=D
@endFrame
M=M-1
A=M
D=M
@THIS
M=D
@endFrame
M=M-1
A=M
D=M
@ARG
M=D
@endFrame
M=M-1
A=M
D=M
@LCL
M=D
@retAddr
A=M
0;JMP

```

