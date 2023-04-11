# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p:str, sufnum:int)-> None:
        """
        Adiciona o sufixo p à Trie e diz-nos qual é a posição no sufnum
        Args:
            p: sufixo a adicionar
            sufnum: posição do sufixo na string original
        """
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():   #percorre a Trie a partir do nó da raiz e adiciona cada caractere da string p que ainda não está presente na Trie
                if pos == len(p)-1:
                    self.add_node(node, p[pos], sufnum)
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]] #adiciona o número do sufixo ao nó correspondente
            pos +=1

    
    def suffix_tree_from_seq(self, text:str)->None:
        """
        Função que cria a árvore de sufixos e adiciona um sufixo em cada iteração, usando a anterior
        Args:
            text: texto que vamos procurar o sufixo
        """
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)
            
    def find_pattern(self, pattern)->list[str]:
        """
        Função que procura padrões usando a Trie
        Args:
            pattern: padrão a procurar na Trie
        Returns:
            lista com os padrões encontrados
        """
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
        else:
            return None
        return self.get_leafes_below(node)



    def get_leafes_below(self, node:int)->list[int]:
        """
        Usa função auxiliar para colecionar todas as folhas abaixo de um dado nó
        Args:
            node: índice do nó onde começa a busca
        Returns:
            lista de inteiros
        """
        res = []
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])            
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print(st.find_pattern("TA"))
    #print(st.repeats(2,2))

test()
print()
test2()
        
            
    
    
