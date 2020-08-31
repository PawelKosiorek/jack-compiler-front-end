import sys
import re
import os
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter

def make_file(filename):
    tokenizer = JackTokenizer()
    tokenizer.read_file(filename)
    tokenizer.divide_into_tokens()
    file_to_write = filename[:-5] + "." + "vm"
    writer = VMWriter(file_to_write)
    parser = CompilationEngine(tokenizer, writer)
    parser.void_subroutines()
    parser.methods_()
    parser.compile_class()
    writer.close()
    

def main():   
    if os.path.isdir(sys.argv[1]):
        directory = sys.argv[1]
        if directory[-1] != "/":
            directory += "/"
        for filename in os.listdir(directory):
            if filename.endswith(".jack"):
                make_file(directory+filename)
    else:
        filename = sys.argv[1]
        if filename.endswith(".jack"):
            make_file(filename)
         
if __name__ == "__main__":
    main()

    
    
