class Parser:
    def __init__(self, file):
        self.file = file
        self.tokens = self.carregar_tokens()
    
    def busca_comando(self):
        return self.tokens.pop(0)

    def ha_comandos(self):
        return self.tokens != []

    def carregar_tokens(self):
        with open(self.file) as f:
            lines = map(lambda line: line.split(), f.readlines())
            tokens = list(filter(lambda x: x[0][0:2] != "//", lines))
            return tokens

    