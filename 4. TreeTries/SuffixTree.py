# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self)->None:
        """
        @brief Construtor da class SuffixTree
        """
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
    
    def print_tree(self)->None:
        """
        @brief Função que imprime a árvore de Trie
        """
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin:int, symbol:str, leafnum:int = -1)->None:
        """
        @brief Função que adiciona um novo nó, se este ainda não existir na árvore
        @param origin: origem do nó
        @param symbol: letra do alfabeto correspondente
        @param leafnum: número da folha, toma valor -1 caso não seja folha
        """
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p:str, sufnum:int)-> None:
        """
        @brief Adiciona o sufixo à Trie e diz-nos qual é a posição no sufnum
        @param p: sufixo a adicionar
        @param sufnum: posição do sufixo na string original
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
        @brief Função que cria a árvore de sufixos e adiciona um sufixo em cada iteração, usando a anterior
        @param text: texto que vamos procurar o sufixo
        """
        t = text+"$" #adiciona o $ no final da seq
        self.seq = t
        for i in range(len(t)):
            self.add_suffix(t[i:], i)
            
    def find_pattern(self, pattern)->list[str]:
        """
        @brief Função que procura se existe um padrão na árvore
        @param pattern: padrão a procurar na Trie
        @return lista com os padrões encontrados
        """
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():  #se as letras estiverem no self.node na pos 0 nas keys
                node = self.nodes[node][1][pattern[pos]]  #troca de node
        else:
            return None
        return self.get_leafes_below(node)



    def get_leafes_below(self, node:int)->list[int]:
        """
        @brief Usa função auxiliar para colecionar todas as folhas abaixo de um dado nó
        @param node: índice do nó onde começa a busca
        @return lista de inteiros
        """
        res = []
        if self.nodes[node][0] >=0: #se o nó 0 não tem valor -1, significa que é uma folha
            res.append(self.nodes[node][0])    #guarda a sua posição         
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
    print (st.find_pattern("TA"))

    
if __name__ == "__main__":
    print("Test 1:")
    test()
    print()
    print("Test 2:")
    test2()
    print()
    print("DONE")
    
    
    
