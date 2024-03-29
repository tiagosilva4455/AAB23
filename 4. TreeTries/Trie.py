# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self)->None:
        """
        @brief Construtor da class Trie
        """
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self)->None:
        """
        @brief Função que imprime a Trie
        """
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin:int, symbol:str)->None:
        """
        @brief Função que adiciona um novo nó
        @param origin: define a origem
        @param symbol: indica a letra presente na posição
        """
        self.num += 1  #contador do número de nós
        self.nodes[origin][symbol] = self.num  #vai buscar o valor associado ao símbolo e o respetivo nó
        self.nodes[self.num] = {}
    
    def add_pattern(self, p:str)-> None:
        """
        @brief Adiciona um padrão à Trie
        @param p: padrão a ser adicionado
        """

        pos = 0    #inicialização da raiz da Trie
        node = 0

        while True:     #percorre cada caractere do padrão
            if p[pos] not in self.nodes[node].keys():   #se o char não estiver presente nas folhas do nó atual, add novo node
                self.add_node(node, p[pos])
            node = self.nodes[node][p[pos]]  #ao novo node atribuímos a nova folha
            pos += 1

            if pos == len(p):  #pos atinge o tamanho do padrão -> break
                break
            
    def trie_from_patterns(self, pats: list[str])->None:
        """
        @brief Adiciona um conjunto de padrões à Trie
        @param pats: lista de padrões a serem adicionados à Trie
        """
        for p in pats:
            self.add_pattern(p) #adiciona cada padrão à Trie
            
    def prefix_trie_match(self, text:str)->None:
        """
        @brief Procura a ocorrência de um dos padrões como prefixo de uma sequência
        @param text: texto para o qual vamos procurar o prefixo
        @return String correspondente ao maior padrão que é prefixo
        """
        pos = 0
        match = ""
        node = 0
        while True:
            if text[pos] in self.nodes[node].keys():  #a cada caractere do texto
                node = self.nodes[node][text[pos]]   #verifica se é  um caractere das folhas do node atual
                match += text[pos]
                if self.nodes[node] == {}:     #se o nó atual não tiver mais folhas, o match é o prefixo
                    return match
                else:
                    pos += 1
            else:
                return None #percorretodo o texto mas não encontra um prefixo
            if pos == len(text):
                break
        return None

    def trie_matches(self, text:str)->list[tuple[int,str]]:
        """
        @brief Procura padrões na sequência text
        @param text: texto que vamos procurar o prefixo
        @return Lista de tuplos (posição inicial do padrão, padrão(str))
        """
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])  #verifica se existe um padrão que começa nessa posição a partir da função prefix_match
            if m != None: res.append((i, m))   #se encontrar o padrão, add à lista res o tuplo com a posição e o padrão
        return res

#tests
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
if __name__ == "__main__":
    print("Test 1:")
    test()
    print()
    print("Test 2:")
    test2()
    print()
    print("DONE")
    