from codeWriter import CodeWriter
from Parser import Parser

ARITHMETICS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


def translate(path, code: CodeWriter):

    p = Parser(path)

    while p.ha_comandos():

        command = p.busca_comando()

        if command[0] == "push":

            code.writePush(command[1], command[2])

        elif command[0] in ARITHMETICS:

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

    path = "StackTest.vm"

    code = CodeWriter(path)

    translate(path, code)


main()
