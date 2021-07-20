// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@24575 // end of screen map
D=A
@last_row
M=D

(MAINLOOP)

    @SCREEN
    D=A
    @addr
    M=D // addr = 16384

    @KBD
    D=M
    @WHITE // if no key is pressed go to WHITE
    D;JEQ

    // else blacken the screen
    (BLACKLOOP)
        @addr
        D=M
        @last_row
        D=D-M
        @MAINLOOP
        D;JGT // if addr >= last_row go to MAINLOOP

        @addr
        A=M
        M=-1 // RAM[addr] = 1111111111111111

        @addr
        M=M+1

        @BLACKLOOP
        0;JMP // go to BLACKLOOP

    (WHITE)
        (WHITELOOP)
            @addr
            D=M
            @last_row
            D=D-M
            @MAINLOOP
            D;JGT // if addr > last_row go to MAINLOOP

            @addr
            A=M
            M=0 // RAM[addr] = 0000000000000000

            @addr
            M=M+1

            @WHITELOOP
            0;JMP // go to WHITELOOP

    @MAINLOOP
    0;JMP