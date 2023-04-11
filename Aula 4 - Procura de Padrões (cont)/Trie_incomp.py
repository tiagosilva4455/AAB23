# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        self.num += 1
        self.nodes[origin][symbol] = self.num
        self.nodes[self.num] = {}
    
    def add_pattern(self, p:str)-> None:
        """
        Adiciona um padrão à Trie
        Args:
            p: padrão a ser adicionado
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
        Adiciona um conjunto de padrões à Trie
        Args:
            pats: lista de padrões a serem adicionados à Trie
        """
        for p in pats:
            self.add_pattern(p) #adiciona cada padrão à Trie
            
    def prefix_trie_match(self, text:str)->None:
        """
        Procura a ocorrência de um dos padrões como prefixo de uma sequência
        Args:
            text: texto para o qual vamos procurar o prefixo
        Returns:
            string correspondente ao maior padrão que é prefixo
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
        Procura padrões na sequência text
        Args:
            text: texto que vamos procurar o prefixo
        Returns:
            Lista de tuplos (posição inicial do padrão, padrão(str))
        """
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])  #verifica se existe um padrão que começa nessa posição a partir da função prefix_match
            if m != None: res.append((i, m))   #se encontrar o padrão, add à lista res o tuplo com a posição e o padrão
        return res
        
          
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
    
test()
print()
test2()
