import sys
import re
import os


class JackTokenizer():

    def __init__(self):
        self.lines = ""
        self.keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int',
                        'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
                        'else', 'while', 'return']
        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<',
                        '>', '=', '~']
        self.types = ["int", "char", "boolean"]

        self.tokens = []

    def read_file(self, filename):
        f =  open(filename, "r")
        lines = f.readlines()    
        f.close()

        comment = False
        for line in lines:
            line = line.strip()
            if "//" in line:
                line = line.split("//")[0]
            if "/**" in line:
                comment = True
            if "*/" in line:
                comment = False
            if comment:
                continue
            if "*/" in line:
                continue
            if re.search(r"\S+", line) == None:
                continue
            self.lines = self.lines + line + "\n"
        return
    
    def divide_into_tokens(self):
        i = 0
        j = 0
        while i < len(self.lines):
            j = 0
            while j < len(self.symbols):   
                if self.lines[i] == self.symbols[j]:
                    item = self.lines[:i:].strip()
                    if not(item.startswith("\"") and item.endswith("\"")):
                        item = item.split(" ")
                        for part in item:    
                            if re.search(r"\S+", part) != None:
                                self.tokens.append(part)
                    else:
                        self.tokens.append(item)
                    self.tokens.append(self.lines[i])
                    self.lines = self.lines[i+1::]
                    i = 0
                    j = 0
                    continue
                j += 1
            i += 1  
        return
            
    def has_more_tokens(self):
        if len(self.tokens) > 0:
            return True
        return False

    def advance(self):
        if self.has_more_tokens():
            current_token = self.tokens[0]
            self.tokens.remove(current_token)
            return current_token
        return "No more tokens"

    def token_type(self, current_token):
        if current_token in self.keywords:
            return "KEYWORD"

        elif current_token in self.symbols:
            return "SYMBOL"

        elif re.match(r"[0-9]+", current_token):
            return "INT_CONST"

        elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", current_token):
            return "IDENTIFIER"

        elif re.match(r"[\".\"]", current_token):
            return "STRING_CONST"

    def key_word(self, token):
        return token

    def symbol(self, token):
        if token == "<":
            return "&lt;"
        elif token == ">":
            return "&gt;"
        elif token == "\"":
            return "&quot;"
        elif token == "&":
            return "&amp;"
        else:
            return token

    def identifier(self, token):
        return token

    def int_val(self, token):
        return int(token)

    def string_val(self, token):
        return token[1:-1:1]