class Parser:
    def __init__(self, file):
        self.file = file  # salva o caminho do arquivo
        # salva os tokens que estão contidos no arquivo
        self.tokens = self.carregar_tokens()

    def busca_comando(self):
        # retorna o primeiro comando da lista de comandos e exclui ele da lista
        return self.tokens.pop(0)

    def ha_comandos(self):
        return len(self.tokens) > 0  # retorna se ainda há comandos na lista

    def carregar_tokens(self):
        with open(self.file) as f:  # abre o arquivo
            # lê todas as linhas do arquivo
            lines = map(lambda line: line.split(), f.readlines())
            # salva todas as linhas que não são comentários (inicio em //)
            tokens = list(filter(lambda x: x[0][0:2] != "//", lines))

            # em uma lista e retorna
            return tokens
