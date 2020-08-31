class SymbolTable():

    def __init__(self):
        self.class_scope = []
        self.subroutine_scope = []
        self.indexes = {"STATIC": -1, "FIELD": -1, "VAR": -1, "ARG": -1}

    def start_class(self):
        self.class_scope = []
        self.indexes["STATIC"] = -1
        self.indexes["FIELD"] = -1

    def start_subroutine(self):
        self.subroutine_scope = []
        self.indexes["VAR"] = -1
        self.indexes["ARG"] = -1
        return

    def define(self, name, vtype, kind):
        self.indexes[kind] += 1
        if kind == "STATIC" or kind == "FIELD":
            self.class_scope.append({"name": name, "type": vtype, "kind": kind, "index": self.indexes[kind]})
           
        if kind == "VAR" or kind == "ARG":
            self.subroutine_scope.append({"name": name, "type": vtype, "kind": kind, "index": self.indexes[kind]}) 

    def var_count(self, kind):
        return self.indexes[kind]

    def kind_of(self, name):
        for item in self.subroutine_scope:
            for key, value in item.items():
                if item["name"] == name:
                    return item["kind"]
        for item in self.class_scope:
            for key, value in item.items():
                if item["name"] == name:
                    return item["kind"]  
        return None
    
    def type_of(self, name):
        for item in self.subroutine_scope:
            for key, value in item.items():
                if item["name"] == name:
                    return item["type"]
        for item in self.class_scope:
            for key, value in item.items():
                if item["name"] == name:
                    return item["type"]  
        return None

    def index_of(self, name):
        for item in self.subroutine_scope:
            for key, value in item.items():
                if item["name"] == name:
                    return item["index"]
        for item in self.class_scope:
            for key, value in item.items():
                if item["name"] == name:
                    return item["index"] 
        return None

    


    