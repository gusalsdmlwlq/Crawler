class Node:
    def __init__(self, node):
        self.type = node[0]
        self.content = node[1]
        if node[2] == "null": self.x = 0
        else: self.x = float(node[2])
        if node[3] == "null": self.y = 0
        else: self.y = float(node[3])
        if node[4] == "null": self.w = 0
        else: self.w = float(node[4])
        if node[5] == "null": self.h = 0
        else: self.h = float(node[5])
        if node[6] == "null": self.fontsize = 0
        else: self.fontsize = float(node[6])
        self.bg_color = node[7]
        self.indent = node[8]