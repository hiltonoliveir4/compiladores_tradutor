class Parser:
    def __init__(self, file):
        self.file = file #salva o caminho do arquivo 
        self.tokens = self.carregar_tokens() #salva os tokens que estão contidos no arquivo 
    
    def busca_comando(self):
        return self.tokens.pop(0) #retorna o primeiro comando da lista de comandos e exclui ele da lista

    def ha_comandos(self):
        return len(self.tokens) > 0 #retorna se ainda há comandos na lista

    def carregar_tokens(self):
        with open(self.file) as f: #abre o arquivo
            lines = map(lambda line: line.split(), f.readlines()) #lê todas as linhas do arquivo
            tokens = list(filter(lambda x: x[0][0:2] != "//", lines))   # salva todas as linhas que não são comentários (inicio em //)
            return tokens                                               # em uma lista e retorna
            

    