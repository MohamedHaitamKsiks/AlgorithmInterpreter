
class Node:
    childs = list()
    def __init__(self,value =None,parent = None):
        self.parent = parent
        self.value = value

    def add_child(self,value):
        #print("child created = ",value)
        child = Node(value = value,parent = self)
        child.childs = list()
        self.childs.append(child)
        if(self.get_parent() != None):
            for k,c in enumerate(self.get_parent().get_child()):
                if c == self:
                    self.parent.childs[k] = self
                    break
        return child

    def get_child(self):
        return self.childs

    def get_parent(self):
        return self.parent

    def get_value(self):
        return self.value

    def set_value(self,val):
        self.value = val

    def has_child(self):
        return len(self.childs)>0

    def draw_tree(self):
        current_node = self
        finish = True
        start_with = 0
        print(current_node.get_value())
        while True:
            finish = True
            for i,child in enumerate(current_node.get_child()[start_with:]) :
                k = start_with+i
                print(current_node.get_value()," => ",child.get_value())
                if child.has_child() :
                    start_with = 0
                    current_node = child
                    finish = False
                    break
            if finish :
                if current_node.get_parent() == None:
                    break
                else :
                    start_with = current_node.get_parent().get_child().index(current_node) + 1
                    current_node = current_node.get_parent()


"""
fam = Node("a")
fam.add_child("1")
fam.add_child("2")
c = fam.add_child("c")
c.add_child("d")
e = c.add_child("e")
e.add_child("f")
e.add_child("m")
fam.add_child("b")

fam.draw_tree()"""
