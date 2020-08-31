import sys
import re
import os
from SymbolTable import SymbolTable


class CompilationEngine():

    def __init__(self, tokenizer, writer):
        self.symbol_table = SymbolTable()
        self.current_keyword = ""
        self.methods = []
        self.voids = ["printInt", "println", "dispose", "setCharAt", "eraseLastChar", "setInt", 
                    "dispose", "init", "moveCursor", "printChar", "printString", "backSpace", 
                    "clearScreen", "setColor", "drawPixel", "drawLine", "drawRectangle", 
                    "drawCircle", "poke", "deAlloc", "halt", "error", "wait"]
        self.current_num_args = 0
        self.label = 0
        self.writer = writer
        self.class_name = ""
        self.current_token = ""
        self.unary = False
        self.tokenizer = tokenizer
    
    def void_subroutines(self):
        for i in range(0, len(self.tokenizer.tokens)):
            if self.tokenizer.tokens[i] == "void":
                self.voids.append(self.tokenizer.tokens[i + 1])
        return

    def methods_(self):
        for i in range(0, len(self.tokenizer.tokens)):
            if self.tokenizer.tokens[i] == "method":
                self.methods.append(self.tokenizer.tokens[i + 2])
        return

    def identifier_check(self):
        if self.tokenizer.token_type(self.class_name) != "IDENTIFIER":
            raise Exception
    
    def void_return(self, name):
        for item in self.voids:
            if item == name:
                self.writer.write_pop("TEMP", 0)
                return
        return


    def eat(self, string):
        if self.current_token != string:
            raise Exception
        self.current_token = self.tokenizer.advance()
        return
    
    def compile_class(self):
        self.symbol_table.start_class()
        self.current_token = self.tokenizer.advance()
        self.eat("class")
        self.class_name = self.current_token
        self.identifier_check()
        self.eat(self.class_name)
        self.eat("{")
        if self.current_token == "}":
            self.eat("}")
            return
        self.compile_class_var_dec()
        self.eat("}") 
        return

    def compile_class_var_dec(self):
        kinds = ["static", "field"]
        types = ["char", "boolean", "int"] 
        symbols = [";",","]
        while self.current_token in kinds:
            for item in kinds:
                if self.current_token == item:
                    var_kind = item
            self.eat(var_kind)
            for item in types:
                if self.current_token == item:
                    var_type = item
            if self.current_token not in types:
                self.identifier_check()
                var_type = self.current_token
            self.eat(var_type)
            self.identifier_check()
            var_name = self.current_token
            self.symbol_table.define(var_name, var_type, var_kind.upper())
            self.eat(var_name)
            if self.current_token == ",":
                while self.current_token != ";":
                    self.eat(",")
                    self.identifier_check()
                    var_name = self.current_token
                    self.symbol_table.define(var_name, var_type, var_kind.upper())
                    self.eat(var_name)
            self.eat(";")
        if self.current_token == "}":
            return
        self.compile_subroutine()
        return
   
    def compile_subroutine(self):
        keywords = ["constructor", "function", "method"]
        types = ["void", "char", "int", "boolean"]
        symbols = ["(", ")", ","]
        self.symbol_table.start_subroutine()
        for item in keywords:
            if self.current_token == item:
                keyword = item
                self.current_keyword = keyword
        self.eat(keyword)
        if self.current_token not in types:
            self.identifier_check()
            return_type = self.current_token
        else:
            for item in types:
                if self.current_token == item:
                    return_type = item
        self.eat(return_type)
        self.identifier_check()
        sub_name = self.current_token
        self.eat(sub_name)
        sub_name = self.class_name + "." + sub_name
        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")
        self.eat("{") 
        self.compile_var_dec()
        self.writer.write_function(sub_name, self.symbol_table.var_count("VAR") + 1)
        if keyword == "constructor" and sub_name == self.class_name + "." + "new":
            self.writer.make_constructor(self.symbol_table.var_count("FIELD") + 1)
        elif keyword == "method":
            self.writer.make_method()
        self.compile_statements()
        self.eat("}")
        if self.current_token != "}":
            self.compile_subroutine()
        return

    def compile_parameter_list(self):
        types = ["void", "char", "int", "boolean"]
        if self.current_keyword == "method":
            self.symbol_table.define("this", self.class_name, "ARG")
        if self.current_token == ")":
            return
        while self.current_token != ")":
            if self.current_token not in types:
                self.identifier_check()
                var_type = self.current_token
            else:
                for item in types:
                    if self.current_token == item:
                        var_type = item
            self.eat(var_type)
            self.identifier_check()
            var_name = self.current_token
            self.eat(var_name)
            self.symbol_table.define(var_name, var_type, "ARG")
            if self.current_token == ",":
                self.eat(",")
                continue
        return

    
    def compile_var_dec(self):
        types = ["void", "char", "int", "boolean"]
        if self.current_token != "var":
           return  
        while self.current_token == "var":
            self.eat("var")
            if self.current_token not in types:
                self.identifier_check()
                var_type = self.current_token
            else:
                for item in types:
                    if self.current_token == item:
                        var_type = item
            self.eat(var_type)     
            self.identifier_check()
            var_name = self.current_token
            self.symbol_table.define(var_name, var_type, "VAR")
            self.eat(var_name)
            while self.current_token != ";":
                self.eat(",")
                self.identifier_check()
                var_name = self.current_token
                self.symbol_table.define(var_name, var_type, "VAR")
                self.eat(var_name)
            self.eat(";")
        return
        
    def compile_statements(self):
        while self.current_token != "}":
            if self.current_token == "return":
                self.compile_return()
                continue
            if self.current_token == "while":
                self.compile_while()
                continue
            if self.current_token == "if":
                self.compile_if()
                continue
            if self.current_token == "do":
                self.compile_do()
                continue
            if self.current_token == "let":
                self.compile_let()
                continue
        return

    def compile_do(self):
        self.eat("do")
        self.identifier_check()
        if self.tokenizer.tokens[0] == "(":
            name = self.current_token
            self.eat(name)
            sub_name = self.class_name + "." + name
            if name in self.methods:
                num_args = self.current_num_args + 1
                self.writer.write_push("POINTER", 0)
            self.eat("(")
            self.compile_expression_list()
            self.eat(")")
            if name in self.methods:
                num_args = self.current_num_args + 1
            else:
                num_args = self.current_num_args
            self.writer.write_call(sub_name, num_args)
            self.void_return(name)
            self.eat(";")
            return
            
        self.identifier_check()
        if self.symbol_table.kind_of(self.current_token) == None:
            class_name = self.current_token
            self.eat(class_name)
            self.eat(".")
            function_name = self.current_token
            self.eat(function_name)
            sub_name = class_name + "." + function_name
            self.eat("(")
            self.compile_expression_list()
            self.eat(")")
            self.writer.write_call(sub_name, self.current_num_args)
            self.void_return(function_name)
            self.eat(";")
            return
            
        if self.symbol_table.kind_of(self.current_token) != None:
            var_name = self.current_token
            self.eat(var_name)
            self.eat(".")
            method_name = self.current_token
            self.eat(method_name)
            class_name = self.symbol_table.type_of(var_name)
            index = self.symbol_table.index_of(var_name)
            kind = self.symbol_table.kind_of(var_name)
            self.writer.write_push(kind, index)
            self.eat("(")  
            self.compile_expression_list()
            self.eat(")")
            self.writer.write_call(class_name + "." + method_name, self.current_num_args + 1)
            self.void_return(method_name)
            self.eat(";")
            return

        return

    def compile_let(self): 
        self.eat("let")
        var_name = self.current_token
        self.identifier_check()
        self.eat(var_name)
        if self.current_token == "[":
            kind = self.symbol_table.kind_of(var_name)
            index = self.symbol_table.index_of(var_name)   
            self.writer.write_push(kind, index)
            self.eat("[")
            self.compile_expression()
            self.eat("]")
            self.writer.write_arithmetic("add")
            self.eat("=")
            self.compile_expression()  
            self.writer.write_pop("TEMP", 0)
            self.writer.write_pop("POINTER", 1)
            self.writer.write_push("TEMP", 0)
            self.writer.write_pop("THAT", 0)
            self.eat(";")
            return
        self.eat("=")
        self.compile_expression()
        index = self.symbol_table.index_of(var_name)
        if self.symbol_table.kind_of(var_name) == "VAR":
            self.writer.write_pop("LOCAL", index)
        elif self.symbol_table.kind_of(var_name) == "ARG":
            self.writer.write_pop("ARG", index)
        elif self.symbol_table.kind_of(var_name) == "FIELD":
            self.writer.write_pop("THIS", index)
        elif self.symbol_table.kind_of(var_name) == "STATIC":
            self.writer.write_pop("STATIC", index)
        self.eat(";")
        return

    def compile_while(self):
        label1 = self.label
        label2 = label1 + 1
        self.label += 100
        self.eat("while")
        self.writer.write_label("L" + str(label1))
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.writer.write_arithmetic("not")
        self.writer.write_if("L" + str(label2))
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.writer.write_goto("L" + str(label1))
        self.writer.write_label("L" + str(label2))
        return

    def compile_return(self):
        self.eat("return")
        if self.current_token != ";":
            self.compile_expression()
            self.writer.write_return()
            self.eat(";")
            return
        self.writer.write_push("CONST", 0)
        self.writer.write_return()
        self.eat(";")
        return

    def compile_if(self):
        label1 = self.label
        label2 = label1 + 1
        self.label += 100
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.writer.write_arithmetic("not")
        self.writer.write_if("L" + str(label1))
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.writer.write_goto("L" + str(label2))
        if self.current_token == "else":
            self.eat("else")
            self.writer.write_label("L" + str(label1))
            self.eat("{")
            self.compile_statements()
            self.eat("}")
        else:
            self.writer.write_label("L" + str(label1))
        self.writer.write_label("L" + str(label2))
        self.label += 1
        return

    def compile_expression(self):
        if self.current_token in ["-", "~"]:
            self.unary = True
        else:
            self.unary = False
        self.compile_term()
        return
        
    def compile_term(self):
        operators = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
        unary_op = ["-", "~"]
        keywords = ["true", "false", "null", "this"]
        symbols = [";", ",", "]", ")"]

        def term():
            if self.current_token in ["-", "~"]:
                self.unary = True
            else:
                self.unary = False 

            if self.unary == True:
                unary_operator = self.current_token
                self.eat(unary_operator)
                term()
                if unary_operator == "~":
                    command = "not"
                else:
                    command = "neg"
                self.writer.write_arithmetic(command)
                return

            if (self.tokenizer.token_type(self.current_token) == "IDENTIFIER") and self.tokenizer.tokens[0] in ["[","(", "."]: 
                if self.tokenizer.tokens[0] == "[":
                    var_name = self.current_token
                    kind = self.symbol_table.kind_of(var_name)
                    index = self.symbol_table.index_of(var_name)
                    self.eat(var_name)
                    self.writer.write_push(kind, index)
                    self.eat("[")
                    self.compile_expression()
                    self.eat("]")
                    self.writer.write_arithmetic("add")
                    self.writer.write_pop("POINTER", 1)
                    self.writer.write_push("THAT", 0)   
                    return

                if self.tokenizer.tokens[0] == "(":
                    sub_name = self.current_token
                    self.eat(sub_name)
                    self.eat("(")
                    self.compile_expression_list()
                    self.eat(")")
                    self.writer.write_call(self.class_name + "." + sub_name, self.current_num_args)
                    self.void_return(sub_name)
                    return
                    
                if self.tokenizer.tokens[0] == ".":
                    if self.symbol_table.kind_of(self.current_token) == None:
                        self.identifier_check()
                        class_name = self.current_token
                        self.eat(class_name)
                    else:
                        var_name = self.current_token
                        self.eat(var_name)
                        self.eat(".")
                        method_name = self.current_token
                        self.eat(method_name)
                        class_name = self.symbol_table.type_of(var_name)
                        index = self.symbol_table.index_of(var_name)
                        kind = self.symbol_table.kind_of(var_name)  
                        self.writer.write_push(kind, index) 
                        self.eat("(")  
                        self.compile_expression_list()
                        self.eat(")")
                        self.writer.write_call(class_name + "." + method_name, self.current_num_args + 1)
                        self.void_return(method_name)  
                        return
                    self.eat(".")
                    sub_name = self.current_token
                    self.eat(sub_name)
                    self.eat("(")  
                    self.compile_expression_list()
                    self.eat(")")      
                    self.writer.write_call(class_name + "." + sub_name, self.current_num_args)
                    self.void_return(sub_name)  
                    return
            if self.current_token == "(": 
                self.eat("(") 
                self.compile_expression()
                self.eat(")")
                return
            if self.tokenizer.token_type(self.current_token) == "IDENTIFIER":
                var_name = self.current_token
                self.eat(var_name)
                if self.symbol_table.kind_of(var_name) == "VAR":
                    segment = "LOCAL"
                elif self.symbol_table.kind_of(var_name) == "ARG":
                    segment = "ARG"
                elif self.symbol_table.kind_of(var_name) == "FIELD":
                    segment = "THIS"
                else:
                    if self.symbol_table.kind_of(var_name) == "STATIC":
                        segment = "STATIC"
                index = self.symbol_table.index_of(var_name)
                
                self.writer.write_push(segment, index)
                return
            if self.tokenizer.token_type(self.current_token) == "INT_CONST":
                integer = self.current_token
                self.eat(integer)
                segment = "CONST"
                self.writer.write_push(segment, integer)
                return       
            if self.tokenizer.token_type(self.current_token) == "STRING_CONST":
                string = self.current_token
                self.eat(string)
                string_length = len(string)
                self.writer.write_push("CONST", string_length)
                self.writer.write_call("String.new", 1)
                for i in range(0, string_length):
                    self.writer.write_push("CONST", ord(string[i]))
                    self.writer.write_call("String.appendChar", 2)
                return
            if self.current_token in keywords:
                keyword = self.current_token
                self.eat(keyword)
                if keyword == "true":
                    self.writer.write_push("CONST", 1)
                    self.writer.write_arithmetic("neg")
                elif keyword == "false":
                    self.writer.write_push("CONST", 0)
                elif keyword == "null":
                    self.writer.write_push("CONST", 0)
                else:
                    self.writer.write_push("POINTER", 0)
                return
    
        while self.current_token not in symbols:
            operator = None
            if self.current_token in operators and self.unary == False:
                operator = self.current_token
                self.eat(operator)
            term()
            if operator != None:
                if operator == "+":
                    command = "add"
                    self.writer.write_arithmetic(command)
                elif operator == "-":
                    command = "sub"
                    self.writer.write_arithmetic(command)
                elif operator == "&":
                    command = "and"
                    self.writer.write_arithmetic(command)
                elif operator == "|":
                    command = "or"
                    self.writer.write_arithmetic(command)
                elif operator == "<":
                    command = "lt"
                    self.writer.write_arithmetic(command)
                elif operator == ">":
                    command = "gt"
                    self.writer.write_arithmetic(command)
                elif operator == "=":
                    command = "eq"
                    self.writer.write_arithmetic(command)
                elif operator == "/":
                    self.writer.write_call("Math.divide", 2)
                elif operator == "*":
                    self.writer.write_call("Math.multiply", 2)
                else:
                    raise Exception
        return
   
    def compile_expression_list(self):
        self.current_num_args = 0  
        while self.current_token != ")":
            self.compile_expression()
            self.current_num_args += 1 
            if self.current_token == ",":
                self.eat(",")
        return