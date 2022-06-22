from node import *
from filemanager import *
import math
import sys
import os

##############################################################################################
class Machine:
    #Variablex
    variables_reel = dict()
    variables_entier = dict()
    variables_charactere = dict()
    variables_chaine = dict()
    variables_bool = dict()
    variables_list = list()
    functions = list()
    #Tree of instructions
    root = Node("root")

    #init
    def __init__(self,filecode):
        #remove com
        while "{" in filecode :
            filecode = filecode.replace(filecode[filecode.find("{"):filecode.find("}")+1],"")
        code = str(filecode).replace("\n","")
        self.load_variables(code)
        self.compile(filecode)
        self.execute()

    #load variables
    def load_variables(self,code):
        #get variables
        vars = code[code.index("VAR")+3:code.index("DEBUT")].split(";")
        for var in vars :
            if var != "" :
                var = var.replace(" ","")
                variable_names = var.split(":")[0]
                #get vaar names
                names = [variable_names]
                if "," in variable_names :
                    names = variable_names.split(",")
                #type
                type = var.split(":")[1]
                #add var
                for name in names :
                    if type == "REEL":
                        self.variables_reel[name] = 0
                        self.variables_list.append(name)
                    elif type == "ENTIER":
                        self.variables_entier[name] = 0
                        self.variables_list.append(name)
                    elif type == "CHARACTERE":
                        self.variables_charactere[name] = ''
                        self.variables_list.append(name)
                    elif type == "CHAINE":
                        self.variables_chaine[name] = ""
                        self.variables_list.append(name)
                    elif type == "BOOL":
                        self.variables_bool[name] = False
                        self.variables_list.append(name)
        self.variables_list.sort(key=len)
        self.variables_list.reverse()
        #print(self.variables_list)

    #get variable
    def get_variable(self,var):
        if var in self.variables_reel.keys() :
            return self.variables_reel[var]
        elif var in self.variables_entier.keys() :
            return self.variables_entier[var]
        elif var in self.variables_charactere.keys()  :
            return self.variables_charactere[var]
        elif var in self.variables_chaine.keys()  :
            return self.variables_chaine[var]
        elif var in self.variables_bool.keys()  :
            return self.variables_bool[var]

    #set variable
    def set_variable(self,var,val):
        if var in self.variables_reel.keys() :
            self.variables_reel[var] = float(eval(self.replace_varname_by_value(val)))
        elif var in self.variables_entier.keys() :
            self.variables_entier[var] = int(eval(self.replace_varname_by_value(val)))
        elif var in self.variables_charactere.keys()  :
            self.variables_charactere[var] = val
        elif var in self.variables_chaine.keys()  :
            self.variables_chaine[var] = val
        elif var in self.variables_bool.keys()  :
            self.variables_bool[var] =bool(eval(self.replace_varname_by_value(val)))

    #interprete lire
    def lire(self,var,val):
        if var in self.variables_reel.keys() :
            self.variables_reel[var] = float(val)
        elif var in self.variables_entier.keys() :
            self.variables_entier[var] = int(val)
        elif var in self.variables_charactere.keys()  :
            self.variables_charactere[var] = val
        elif var in self.variables_chaine.keys()  :
            self.variables_chaine[var] = val
        elif var in self.variables_bool.keys()  :
            self.variables_bool[var] =bool(val)

    #dont start with space
    def dont_start_with_space(self,line):
        line = str(line)
        if len(line) > 0 :
            while line[0] == " ":
                line = line[1:]
        return line

    #small eval
    def replace_varname_by_value(self,line):
        line = line.replace("racine","///")
        line = line.replace("abs","//.//")
        line = line.replace("non","not")
        line = line.replace("et","and")
        line = line.replace("ou","or")
        #replace var
        for name in self.variables_list :
            if name in line :
                line = str(line).replace(name,str(self.get_variable(name)))

        #fonct predifinie
        line = self.predif_func(line)
        #print(line)
        return line

    #predif func
    def predif_func(self,line):
        line = str(line)
        #print(line)
        #square root
        while "///" in line :
            index_start = line.find("///(")
            index_end = line[index_start:].find(")")+index_start
            calcul = line[index_start+4:index_end]
            result = str(math.sqrt(eval(calcul)))
            line = line.replace(line[index_start:index_end+1],result,1)
        #abs
        while "//.//" in line :
            index_start = line.find("//.//(")
            index_end = line[index_start:].find(")")+index_start
            calcul = line[index_start+7:index_end]
            result = str(abs(eval(calcul)))
            line = line.replace(line[index_start:index_end+1],result,1)
        return line

    #compile code
    def compile(self,filecode):
        #prepare code
        code = filecode.splitlines()
        #print(code)
        code = code[code.index("DEBUT")+1:code.index("FIN")]
        #erase space
        for k,line in enumerate(code):
            code[k] = self.dont_start_with_space(line)

        #creating tree from the code
        current_node = self.root
        previous_node = self.root
        for line in code :
            if line.find("SINON") == 0:
                current_node = (current_node.get_parent())
                child = current_node.add_child(previous_node.get_value().replace("SI","SI not(").replace("ALORS",") ALORS"))
                current_node = child
            elif line.find("SI") == 0:
                child = current_node.add_child(line)
                current_node = child
                previous_node = current_node
            elif line.find("TANTQUE") == 0:
                child = current_node.add_child(line)
                current_node = child
            elif line.find("POUR") == 0:
                line_list = line.split(" ")
                #get variable
                var = line_list[1].replace(" ","")
                #start loop
                start = line_list[line_list.index("DE")+1] + "-1"
                #step
                step = 1
                if "PAS" in line_list :
                    step = line_list[line_list.index("PAS")+1]
                #end loop
                end = line_list[line_list.index("A")+1] + '-' + step
                #print(self.replace_varname_by_value(line_list[line_list.index("A")+1]))
                #init var
                current_node.add_child(var+"<-"+str(start)+";")
                #add TANTQUE
                child = current_node.add_child("TANTQUE "+var+" <= "+str(end)+" FAIRE")
                current_node = child
                current_node.add_child(var+"<-"+var+"+"+str(step)+";")
            elif line.find("FINSI") == 0:
                #child = current_node.add_child(line)
                current_node = current_node.get_parent()
            elif line.find("FINTANTQUE") == 0 or line.find("FINPOUR") == 0:
                child = current_node.add_child("FINTANTQUE")
                current_node = current_node.get_parent()
            elif ";" in line:
                child = current_node.add_child(line)

        #self.root.draw_tree()

    #execute code
    def execute(self):
        current_node = self.root
        start_with = 0
        finish = True
        #Browse the root tree
        while True:
            for i,child in enumerate(current_node.get_child()[start_with:]) :
                k = start_with+i
                line = str(child.get_value())
                #execute instructions
                #print("line = ",line)
                finish = True
                if line[len(line)-1] == ";":
                    self.execute_instruction(line[:len(line)-1])
                #condition
                if line.find("SI") == 0:
                    condition = eval(self.replace_varname_by_value(line[3:line.find("ALORS")]))
                    #if condition is verif
                    if condition :
                        start_with = 0
                        current_node = child
                        finish = False
                        break

                #loop while 'TANTQUE'
                ##start the loop
                if line.find("TANTQUE") == 0:
                    condition = eval(self.replace_varname_by_value(line[7:line.find("FAIRE")]))
                    #if condition is verif
                    if condition :
                        start_with = 0
                        current_node = child
                        finish = False
                        break

                #go back to start
                if line.find("FINTANTQUE") == 0:
                    start_with = current_node.get_parent().get_child().index(current_node)
                    current_node = current_node.get_parent()
                    finish = False
                    break

            #go back to parent
            if finish :
                if current_node.get_parent() != None :
                    start_with = current_node.get_parent().get_child().index(current_node) + 1
                else :
                    start_with = 0
                current_node = current_node.get_parent()

            if current_node == None :
                break

    #execute line
    def execute_instruction(self,line):
        #print(line)
        if line.find("ecrire(") == 0 :
            result = ""
            objects = line[7:len(line)-1]
            objects_list = objects.split(",")
            for obj in objects_list:
                if obj[0] == '"' and obj[len(obj)-1] == '"' :
                    result += obj[1:len(obj)-1]
                else :
                    if obj in self.variables_entier or obj in self.variables_reel :
                        result += str(eval(self.replace_varname_by_value(obj)))
                    else :
                        result += str(self.replace_varname_by_value(obj))
            print(result)
        elif line.find("lire(") == 0 :
            objects = line[5:len(line)-1]
            objects_list = objects.split(",")
            for obj in objects_list:
                val = input()
                self.lire(obj, val)
        else :
            var_list = line.split("<-")
            self.set_variable(var_list[0],var_list[1])


##############################################################################################
#file = read_file(sys.argv[1])
file = read_file("test.algo")
#print(sys.argv[0])
machine = Machine(file)
