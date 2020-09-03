# Jack Compiler front end

Jack is a modern, Java-like, high level object oriented language. It was created for the purposes of nand2tetris course and is run on the Hack Computer hardware platform. This software is the front-end part of Jack compiler. Jack compiler consists of back and front end because it is a two-tier one. The front-end part compiles Jack classes into intermadiate code called VM (similar to JVM) whereas the back-end part compiles VM files into a single Hack assembly file, runnable on the Hack platform.

This part of the compiler comprises the following modules:

JackTokenizer, which breaks down input stream into separate Jack-language tokens.

CompilationEngine, which is gets input from JackTokenizer and emits .vm output using recursive descent parsing.

SymbolTable, which provides a symbol table for the compiler.



Please visit www.nand2tetris.org for more information.

Installation
Please do:

$ git clone https://github.com/PawelKosiorek/jack-compiler-back-end.git

Usage
If you invoke $ VMTranslator <filename.vm> the program will create a single <filename.asm> file in the same directory.

If you invoke $ VMTranslator <directoryname> it will compile every .vm file in that directory to one .asm file which will be stored in the same directory.

