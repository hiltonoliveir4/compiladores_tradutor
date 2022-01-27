from codeWriter import CodeWriter
from Parser import Parser

funcoes_aritmeticas = [
        "add", 
        "sub", 
        "neg", 
        "eq", 
        "gt", 
        "lt", 
        "and", 
        "or", 
        "not"
    ]

def translate(path, code: CodeWriter):
    p = Parser(path)
    while p.ha_comandos():
        command = p.busca_comando()
        if command[0] == "push":
            code.writePush(command[1], command[2])
        elif command[0] in funcoes_aritmeticas:
            code.writeArithmetic(command)
        elif command[0] == "pop":
            code.writePop(command[1], command[2])
        elif command[0] == "label":
            code.write_label(command[1])
        elif command[0] == "goto":
            code.write_goto(command[1])
        elif command[0] == "if-goto":
            code.write_if(command[1])
        elif command[0] == "return":
            code.write_return()
        elif command[0] == "call":
            code.write_call(command[1], command[2])
        elif command[0] == "function":
            code.write_function(command[1], command[2])
        else:
            print('Command unexpected', command)


def main():
    import sys
    from os import path, listdir

    try:
        if path.isdir(sys.argv[1]):
            files = listdir(sys.argv[1])
            realPath = path.realpath(sys.argv[1])
            for file in files:
                if file.endswith('.jack'):
                    fileName = realPath+"/"+file
                    print ("compiling",fileName)
                    path = fileName
        elif path.isfile(sys.argv[1]):
            path = sys.argv[1]
            print (sys.argv[1])
        else:
            raise FileNotFoundError
        
    except FileNotFoundError:
        print("File not found.")
    
    code = CodeWriter(path)
    translate(path, code)

main()
