
#read a file
def read_file(path):
    out = ""
    with open(path) as file :
        out = file.read()
    return out
