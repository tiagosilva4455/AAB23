# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class DeBruijnGraph (MyGraph):
    
    def __init__(self, frags:str) -> None:
        '''
        @brief Construtor da classe DeBruijnGraph
        @param frags: fragmentos do genoma
        '''
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o:str, d:str)-> None:
        '''
        @brief Adiciona uma aresta ao grafo.
        @param o: Vertice de origem
        @param d: Vertice de destino
        '''
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    def in_degree(self, v:str)-> int:
        '''
        @brief Calcula o in-degree de um vertice no grafo.
        @param v: vertice
        @returns O in-degree de um vertice.
        '''
        res = 0
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res += self.graph[k].count(v)
        return res

    def create_deBruijn_graph(self, frags:str)-> None:
        '''
        @brief Cria o grafo De Bruijn utilizando os fragmentos dados.
        @param frags: Fragmentos do genoma
        '''
        for sequence in frags:
            suffix = suffix(sequence)
            self.add_vertex(suffix)
            prefix = prefix(sequence)
            self.add_vertex(prefix)
            self.add_edge(prefix,suffix)

    def seq_from_path(self, path:list[str])->str:
        '''
        @brief Constroi uma sequência de um dado caminho no grafo de De Bruijn.
        @param path: lista de vertices que representam o caminho
        @return A sequência construida.
        '''
        seq = path[0]
        for i in range(1,len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq 
    
def suffix (seq:str)->str:
    '''
    @brief Retorna o sufixo de uma sequência
    @param seq: A sequência input
    @returns O sufixo da sequência
    '''
    return seq[1:]
    
def prefix(seq:str)->str:
    '''
    @brief Retorna o prefixo de uma sequência
    @param seq: A sequência input
    @returns O preixo da sequência
    '''
    return seq[:-1]

def composition(k:int, seq:str)->list[str]:
    '''
    @brief Gera a composição com tamnaho de k da sequência.
    @param k: tamanho de cada subsequência
    @param seq: A sequência input
    @returns A lista de subsequencia de tamanho k
    '''
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res



def test1():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    
    
def test2():
frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
dbgr = DeBruijnGraph(frags)
dbgr.print_graph()
print (dbgr.check_nearly_balanced_graph())
print (dbgr.eulerian_path())


def test3():
    orig_sequence = "ATGCAATGGTCTG"
    frags = composition(3, orig_sequence)
    # ... completar



test1()
print()
#test2()
#print()
#test3()
    
