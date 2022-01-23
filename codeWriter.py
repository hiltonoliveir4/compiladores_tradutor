class CodeWriter:

    def __init__(self, path):
        self.path = f"{path.replace('.vm','.asm')}"
        self.output = open(self.path)
        self.module_name = path.split("/")[-1].replace(".vm", "")
        self.func_name = ""
        self.label_count = 0
        self.call_count = 0
        self.return_sub_count = 0

        with open(self.path, "w") as f:
            f.write("")

    def write(self, valor):

        with open(self.path, "a") as f:
            f.write(valor + "\n")

    def segmentPointer(self, seg, index):
        if seg == "local":
            return "LCL"
        elif seg == "argument":
            return "ARG"
        elif seg == "this" or seg == "that":
            return seg.upper()
        elif seg == "temp":
            return self.write("R{}\n".format(5+int(index)))
        elif seg == "pointer":
            return self.write("R{}\n".format(3+int(index)))
        elif seg == "static":
            return self.write("{}".format(index))
        else:
            return "ERROR"

    def writeInit(self):
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
        self.write("Sys.init", 0)
        # self.writeSubRotineReturn()
        self.writeSubArithmeticLt()
        self.writeSubArithmeticGt()
        self.writeSubArithmeticEq()
        # self.writeSubFrame()

    def writeSubArithmeticEq(self):
        self.write("($EQ$)")
        self.write("@R15")
        self.write("M=D")

        label = self.write(
            "JEQ_{}_{}\n".format(self.module_name, self.label_count))
        self.write("@SP // eq")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write("@" + label)
        self.write("D;JEQ")
        self.write("D=1")
        self.write("(" + label + ")")
        self.write("D=D-1")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")

        self.label_count += 1

        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def writeSubArithmeticGt(self):
        self.write("($GT$)")
        self.write("@R15")
        self.write("M=D")

        labelTrue = self.write(
            "JGT_TRUE_{}_{}\n".format(self.module_name, self.label_count))
        labelFalse = self.write(
            "JGT_FALSE_{}_{}\n".format(self.module_name, self.label_count))

        self.write("@SP // gt")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write("@" + labelTrue)
        self.write("D;JGT")
        self.write("D=0")
        self.write("@" + labelFalse)
        self.write("0;JMP")
        self.write("(" + labelTrue + ")")
        self.write("D=-1")
        self.write("(" + labelFalse + ")")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")

        self.label_count += 1

        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def writeSubArithmeticLt(self):
        self.write("($LT$)")
        self.write("@R15")
        self.write("M=D")

        labelTrue = self.write(
            "JLT_TRUE_{}_{}\n".format(self.module_name, self.label_count))
        labelFalse = self.write(
            "JLT_FALSE_{}_{}\n".format(self.module_name, self.label_count))

        self.write("@SP // lt")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write("@" + labelTrue + "")
        self.write("D;JLT")
        self.write("D=0")
        self.write("@" + labelFalse + "")
        self.write("0;JMP")
        self.write("(" + labelTrue + ")")
        self.write("D=-1")
        self.write("(" + labelFalse + ")")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")

        self.label_count += 1

        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def writePush(self, segment, index):
        print(segment)
        print(index)
        if segment == "constant":
            self.write(f"@{index} // push {segment} {index}")
            self.write("D=A")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M = M + 1")
        elif segment == "static" or segment == "temp" or segment == "pointer":
            self.write(
                "{} //" + " push {} {}" .format(self.segmentPointer(segment, index), segment, index))
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            self.write(
                "{} //" + " push {} {}" .format(self.segmentPointer(segment, index), segment, index))
            self.write("D=M")
            self.write("{}" .format(index))
            self.write("A=D+A")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        else:
            pass

    def writePop(self, segment, index):
        if segment == "static" or segment == "temp" or segment == "pointer":
            self.write(
                "@SP //" + " pop {} {}" .format(segment, index))
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write(
                "{}" .format(self.segmentPointer(segment, index)))
            self.write("M=D")
        elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            self.write(
                f"@{self.segmentPointer(segment, index)} // pop {segment} {index}")
            self.write("D=M")
            self.write("{}" .format(index))
            self.write("D=D+A")
            self.write("@R13")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@R13")
            self.write("A=M")
            self.write("M=D")
        else:
            pass

    def writeArithmetic(self, cmd):
        if cmd[0] == "add":
            self.writeArithmeticAdd()
        elif cmd[0] == "sub":
            self.writeArithmeticSub()
        elif cmd[0] == "neg":
            self.writeArithmeticNeg()
        elif cmd[0] == "eq":
            self.writeArithmeticEq()
        elif cmd[0] == "gt":
            self.writeArithmeticGt()
        elif cmd[0] == "lt":
            self.writeArithmeticLt()
        elif cmd[0] == "and":
            self.writeArithmeticAnd()
        elif cmd[0] == "or":
            self.writeArithmeticOr()
        elif cmd[0] == "not":
            self.writeArithmeticNot()
        else:
            pass

    def writeBinaryArithmetic(self):
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("A=A-1")

    def writeArithmeticAdd(self):
        self.writeBinaryArithmetic()
        self.write("M=D+M")

    def writeArithmeticSub(self):
        self.writeBinaryArithmetic()
        self.write("M=M-D")

    def writeArithmeticAnd(self):
        self.writeBinaryArithmetic()
        self.write("M=D&M")

    def writeArithmeticOr(self):
        self.writeBinaryArithmetic()
        self.write("M=D|M")

    def writeUnaryArithmetic(self):
        self.write("@SP")
        self.write("A=M")
        self.write("A=A-1")

    def writeArithmeticNeg(self):
        self.writeUnaryArithmetic()
        self.write("M=-M")

    def writeArithmeticNot(self):
        self.writeUnaryArithmetic()
        self.write("M=!M")

    def writeArithmeticEq(self):
        returnAddr = self.output.writelines(
            "$RET{}" .format(self.returnSubCount))
        self.write(self.output.writelines("@{}" .format(self.returnAddr)))
        self.write("D=A")
        self.write("@EQ$")
        self.write("0;JMP")
        self.write(self.output.writelines("{}" .format(self.returnAddr)))
        self.returnSubCount = self.returnSubCount + 1

    def writeArithmeticGt(self):
        returnAddr = self.output.writelines(
            "$RET{}" .format(self.returnSubCount))
        self.write(self.output.writelines("@{}" .format(self.returnAddr)))
        self.write("D=A")
        self.write("@$GT$")
        self.write("0;JMP")
        self.write(self.output.writelines("{}" .format(self.returnAddr)))
        self.returnSubCount = self.returnSubCount + 1

    def writeArithmeticLt(self):
        returnAddr = self.output.writelines(
            "$RET{}" .format(self.returnSubCount))
        self.write(self.output.writelines("@{}" .format(self.returnAddr)))
        self.write("D=A")
        self.write("@$LT$")
        self.write("0;JMP")
        self.write(self.output.writelines("{}" .format(self.returnAddr)))
        self.returnSubCount = self.returnSubCount + 1

    def writeClose(self):
        self.path.Close()
