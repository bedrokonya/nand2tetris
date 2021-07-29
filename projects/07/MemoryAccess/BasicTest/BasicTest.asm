// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@10

D=A

@SP

A=M

M=D

@SP

M=M+1
// pop segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@0

D=A

@LCL

D=M+D

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D
// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@21

D=A

@SP

A=M

M=D

@SP

M=M+1
// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@22

D=A

@SP

A=M

M=D

@SP

M=M+1
// pop segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@2

D=A

@ARG

D=M+D

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D
// pop segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@1

D=A

@ARG

D=M+D

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D
// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@36

D=A

@SP

A=M

M=D

@SP

M=M+1
// pop segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@6

D=A

@THIS

D=M+D

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D
// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@42

D=A

@SP

A=M

M=D

@SP

M=M+1
// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@45

D=A

@SP

A=M

M=D

@SP

M=M+1
// pop segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@5

D=A

@THAT

D=M+D

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D
// pop segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@2

D=A

@THAT

D=M+D

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D
// push constant i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i)



@510

D=A

@SP

A=M

M=D

@SP

M=M+1
// pop temp i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_addr)

// where segment_addr is base location of temp segment in RAM



@5

D=A

@6

D=D+A

@addr

M=D

@SP

M=M-1

A=M

D=M

@addr

A=M

M=D

// push segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



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

// push segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@5

D=A

@THAT

A=M+D

D=M

@SP

A=M

M=D

@SP

M=M+1

//add

@SP

A=M-1

D=M       // D = *(SP-1)

A=A-1

M=D+M     // M = *(SP-1) + *(SP-2)

@SP

M=M-1       // SP--
// push segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



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

//sub

@SP

A=M-1

D=M       // D = *(SP-1)

A=A-1

M=M-D     // M = *(SP-2) - *(SP-1)

@SP

M=M-1     // SP--
// push segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@6

D=A

@THIS

A=M+D

D=M

@SP

A=M

M=D

@SP

M=M+1

// push segment i

// where segment = local/argument/this/that

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_asm)

// where segment_asm == LCL/ARG/THIS/THAT



@6

D=A

@THIS

A=M+D

D=M

@SP

A=M

M=D

@SP

M=M+1

//add

@SP

A=M-1

D=M       // D = *(SP-1)

A=A-1

M=D+M     // M = *(SP-1) + *(SP-2)

@SP

M=M-1       // SP--
//sub

@SP

A=M-1

D=M       // D = *(SP-1)

A=A-1

M=M-D     // M = *(SP-2) - *(SP-1)

@SP

M=M-1     // SP--
// push temp i

// When used in runtime the content of curly brackets is removed via CommandTranslationProvider

// and the string with content of this file needs to be formatted in order to be valid asm program:

//           ' ..this file content.. '.format(i, segment_addr)

// where segment_addr is base location of temp segment in RAM



@5

D=A

@6

D=D+A

A=D

D=M

@SP

A=M

M=D

@SP

M=M+1

//add

@SP

A=M-1

D=M       // D = *(SP-1)

A=A-1

M=D+M     // M = *(SP-1) + *(SP-2)

@SP

M=M-1       // SP--
