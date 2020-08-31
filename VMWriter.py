
class VMWriter():

    def __init__(self, file_to_write):
        self.file = file_to_write
        self.f = open(self.file, "w")
        return
        
    def write_push(self, segment, index):
        if segment == "CONST":
            print("push", "constant", index, file = self.f)
        elif segment == "LOCAL":
            print("push", "local", index, file = self.f)
        elif segment == "ARG":
            print("push", "argument", index, file = self.f)
        elif segment == "VAR":
            print("push", "local", index, file = self.f)
        elif segment == "POINTER":
            if index not in [0, 1]:
                raise Exception
            print("push", "pointer", index, file = self.f)
        elif segment == "THIS":
            print("push", "this", index, file = self.f)
        elif segment == "THAT":
            print("push", "that", index, file = self.f)
        elif segment == "STATIC":
            print("push", "static", index, file = self.f)
        elif segment == "FIELD":
            print("push", "this", index, file = self.f)
        elif segment == "TEMP":
            print("push", "temp", index, file = self.f)
        return

    def write_pop(self, segment, index):
        if segment == "TEMP":
            print("pop", "temp", index, file = self.f)
        elif segment == "LOCAL":
            print("pop", "local", index, file = self.f)
        elif segment == "ARG":
            print("pop", "argument", index, file = self.f)
        elif segment == "VAR":
            print("pop", "local", index, file = self.f)
        elif segment == "POINTER":
            if index not in [0, 1]:
                raise Exception
            print("pop", "pointer", index, file = self.f)
        elif segment == "THIS":
            print("pop", "this", index, file = self.f)
        elif segment == "THAT":
            print("pop", "that", index, file = self.f)
        elif segment == "STATIC":
            print("pop", "static", index, file = self.f)
        elif segment == "FIELD":
            print("pop", "this", index, file = self.f)
        return

    def write_arithmetic(self, command):
        print(command, file = self.f)
        return

    def write_label(self, string):
        print("label", string, file = self.f)
        return

    def write_goto(self, string):
        print("goto", string, file = self.f)
        return

    def write_if(self, string):
        print("if-goto", string, file = self.f)
        return
    
    def write_call(self, name, num_args):
        print("call", name, num_args, file = self.f)
        return
    
    def make_constructor(self, field_count):
        self.write_push("CONST", field_count)
        self.write_call("Memory.alloc", 1)
        self.write_pop("POINTER", 0)
        return
    
    def make_method(self):
        self.write_push("ARG", 0)
        self.write_pop("POINTER", 0)
        return
    
    def write_function(self, name, num_locals):
        print("function", name, num_locals, file = self.f)
        return
    
    def write_return(self):
        print("return", file = self.f)
        return
    
    def close(self):
        self.f.close()
        return

    
    
    