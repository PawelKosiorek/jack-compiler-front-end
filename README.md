# Jack Compiler front end

Jack is a modern, Java-like, high level object oriented language. It was created for the purposes of Nand2tetris course and is run on the Hack Computer hardware platform. This software is the front-end part of Jack compiler. Jack compiler consists of back and front end because it is a two-tier one. The front-end part compiles Jack classes into intermadiate code called VM (similar to JVM) whereas the back-end part compiles VM files into a single Hack assembly file, runnable on the Hack platform.

This part of the compiler comprises the following modules:

JackTokenizer, which breaks down input stream into separate Jack-language tokens.

CompilationEngine, which is a recursive top-down compilation engine.

SymbolTable, which provides a symbol table for the compiler.

VMWrite, which emits VM commands into a file.

JackCompiler, which is a top-level driver that invokes the other modules.



Please visit www.nand2tetris.org for more information.

### Installation
Please do:

`$ git clone https://github.com/PawelKosiorek/jack-compiler-front-end.git`

### Usage

You will need the Nand2tetris Software Suite to run Jack programs. Get it from https://www.nand2tetris.org/software

If you invoke `$ python3 JackCompiler <filename.jack>` the program will create a single <filename.vm> file in the same directory.

If you invoke `$ python3 JackCompiler <directoryname>` it will compile every Jack class in that directory and store the corresponding .vm files in the same directory.

