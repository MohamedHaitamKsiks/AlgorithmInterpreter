from tkinter import *
from tkinter.filedialog import *
from interpreteur.filemanager import *
from tkinter.messagebox import *

import os
import sys

#vars
file = "untitled.algo"
save = False
dark = False

#const
menu_elements = dict()
################################################################################
#prepare window
window = Tk()
window.title(file)

window.resizable(0,0)


#line
select = Label(window , text = "(1.0)")

#text area
text_code = Text(window)
text_code.config(width = 80,height = 40)
scrollb = Scrollbar(command=text_code.yview)
text_code['yscrollcommand'] = scrollb.set
scrollb.pack(side = RIGHT , fill = Y)

#fonctions
def Nouveau():
    #reset text
    global text_code
    text_code.delete("1.0",END)
    line.config(text="("+text_code.index("insert")+")")
    #set file
    global file
    file = "untitled.algo"
    #set save
    global save
    save = False
    window.title("untitled.algo")

def Ouvrir():
    #open file
    filename = askopenfilename(title = "Ouvrir un algorthme",filetypes = [("fichier algorithme (*.algo)",".algo")])
    if filename != "" :
        global text_code
        text_code.delete("1.0",END)
        text_code.insert(INSERT,read_file(filename))
        global file
        file = filename
        #set save
        global save
        save = True
        #changetitle
        global window
        window.title(file)
        Color_code("")

def Enregistrer():
    global save
    if save :
        global text_code
        global file
        with open(file,"w") as f :
            f.write(text_code.get("1.0",END))
    else :
        Enregistrer_Sous()

def Enregistrer_Sous():
    filename = asksaveasfilename(title = "Enregistrer_sous",filetypes = [("fichier algorithme (*.algo)",".algo")])
    if filename != "" :
        filename += ".algo"
        #save
        global text_code
        with open(filename,"w") as f :
            f.write(text_code.get("1.0",END))
        global file
        file = filename
        global save
        save = True
        window.title(file)

def Execute(file,save):
    if save :
        os.system('./execute.sh "'+file+'"')

def Save_Execute(file,save):
    if save :
        Enregistrer()
        os.system('./execute.sh "'+file+'"')

def add_token(token,color):
    pos_start = text_code.search(token, '1.0', END)
    pos_end = pos_start
    while pos_start != "":
        pos_end = pos_start.split(".")[0] + "." + str(int(pos_start.split(".")[1])+len(token))
        text_code.tag_add(color+"_tag",pos_start,pos_end)
        pos_start = text_code.search(token, pos_end, END)
    text_code.tag_config(color+"_tag",foreground = color)

def add_token_list(token_list,color):
    text_code.tag_remove(color+"_tag","1.0",END)
    for token in token_list :
        add_token(token,color)

def add_long_token(token,color):
    text_code.tag_remove(color+"_tag","1.0",END)
    pos_start = text_code.search(token[0], '1.0', END)
    pos_end = text_code.search(token[1], '1.0', END)
    while pos_start != "" and pos_end != "":
        start = pos_start.split(".")[0] + "." + str(int(pos_start.split(".")[1])+1)
        try :
            pos_end = text_code.search(token[1], start, END)
            pos_end = pos_end.split(".")[0] + "." + str(int(pos_end.split(".")[1])+1)
        except IndexError :
            break
        text_code.tag_add(color+"_tag",pos_start,pos_end)
        pos_start = text_code.search(token[0], pos_end, END)
    text_code.tag_config(color+"_tag",foreground = color)

def Color_code(event):
    select.config(text="("+text_code.index("insert")+")")
    #operation token
    add_token_list(['+','-','*','/','<-','%','non','et','ou',':','>','<','='],"magenta2")
    #condition loop
    if dark :
        add_token_list(['SI','ALORS','SINON','FINSI','TANTQUE','FAIRE','FINTANTQUE','POUR','DE','A','PAS','FINPOUR','DEBUT','FIN','VAR'],"orange red")
        add_token_list(['lire','ecrire','racine','abs'],"orange")
        add_long_token('""',"spring green")
    else :
        add_token_list(['SI','ALORS','SINON','FINSI','TANTQUE','FAIRE','FINTANTQUE','POUR','DE','A','PAS','FINPOUR','DEBUT','FIN','VAR'],"red")
        add_token_list(['lire','ecrire','racine','abs'],"blue")
        add_long_token('""',"green")
    #comment
    add_long_token("{}","gray50")

def set_dark(val):
    if val :
        text_code.config(bg = "#46474f" ,fg = "white")
        window.config(bg = "#282930")
        select.config(bg = "#282930", fg = "white")
    else :
        text_code.config(bg = "white" ,fg = "black")
        window.config(bg = "gray90")
        select.config(bg = "gray90", fg = "black")
    global dark
    dark = val
    Color_code("")

#menu bar
menu_bar = Menu(window)
#File
menu_file = Menu(window,tearoff = 0)
menu_bar.add_cascade(label = "Fichier",menu = menu_file)
menu_file.add_command(label="Nouveau <Control-N>",command = Nouveau)
menu_file.add_command(label="Ouvrir <Control-O>" ,command = Ouvrir)
menu_file.add_command(label="Enregistrer <Control-S>",command = Enregistrer)
menu_file.add_command(label="Enregistrer-sous <Control-Alt-S>",command = Enregistrer_Sous)
menu_file.add_separator()
menu_file.add_command(label="Quiter",command = sys.exit)

#style
menu_style = Menu(window,tearoff = 0)
menu_bar.add_cascade(label = "Style",menu = menu_style)
menu_style.add_command(label="Light",command = lambda : set_dark(False))
menu_style.add_command(label="Dark" ,command = lambda : set_dark(True))

#Run
menu_run = Menu(window,tearoff = 0)
menu_bar.add_cascade(label = "Executer",menu = menu_run)
menu_run.add_command(label="Executer <F5>",command = lambda :Execute(file,save))
menu_run.add_command(label="Enregister et executer <F6>" ,command = lambda :Save_Execute(file,save))


#change color
window.bind("<Key>",Color_code)
window.bind("<F5>",lambda event : Execute(file,save))
window.bind("<F6>",lambda event : Save_Execute(file,save))
window.bind("<Control-s>",lambda event : Enregistrer())
window.bind("<Control-n>",lambda event :Nouveau())
window.bind("<Control-o>",lambda event :Ouvrir())
window.bind("<Control-Alt-s>",lambda event :Enregistrer_Sous())


#pack
window.config(menu = menu_bar)
text_code.pack()
select.pack(anchor = "w",padx = 10)

#start the window
window.mainloop()
