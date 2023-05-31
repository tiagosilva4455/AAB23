# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class OverlapGraph(MyGraph):
 
    def __init__(self, frags, reps = False):
        MyGraph.__init__(self,{})
        if reps: 
            self.create_overlap_graph_with_reps(frags)
        else: 
           self.create_overlap_graph(frags)
        self.reps = reps
        
    
    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags:list[str])->None:
        """
        @brief Cria um grago de sobreposição com base numa lista de fragmentos
        @param frags:lista de fragmentos da sequência
        """
        for x in frags: #por sequencia em frag
            self.add_vertex(x)  #cria vértice no grafo
        for seq in frags:
                sufixo = suffix(seq)  #verifica qual é o sufixo da seq, ou seja todas as letras exceto a primeira da seq
                for seq2 in frags:
                    if prefix(seq2) == sufixo: #se o prefixo, ou seja tudo menos a ultima letra, é igual ao sufixo
                        self.add_edge(seq,seq2) #adiciona um edge que é um tuplo  (sufixo,prefixo)

        
    def create_overlap_graph_with_reps(self, frags:list[str])->None:  # caso de replicas de fragmentos
        """
        @brief Cria um grafo de sobreposição com base em uma lista de fragmentos, tendo em consideração fragmentos replicados.
        @param frags: lista de fragmentos da sequência
        """
        idnum = 1
        for seq in frags:
            self.add_vertex(seq + '-' + str(idnum)) #vai adicionar o vértice com a sequencia + um identificador associado que começa em 1
            idnum += 1
        idnum = 1 #para adicionar os edges recomeçamos a contagem do idnum
        for seq in frags:
            sufixo = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == sufixo: #se o prefixo for igual ao sufixo
                    for y in self.get_instances(seq2): #por cada y em get_instances
                        self.add_edge(seq + '-' + str(idnum), y) #adicionar edges ao vértice, primeiro damos o vértice de origem (seq+'-'+str(idnum)) e depois
                        #o de destino que vai ser o y que  cada elemento vindo da lista da função get_instances
            idnum += 1
    
    def get_instances(self, seq:str)->list[str]:
        """
        @brief Retorna uma lista contendo todas as instâncias de uma sequência no grafo
        @param seq: sequência
        @return lista de instância da sequência
        """
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res
    
    def get_seq(self, node:str)->str or None:
        """
        @brief Retorna a sequência associada a um nó do grafo
        @param node: nó do grafo
        @return A sequência associada ao nó ou None se o nó não existir no grafo
        """
        if node not in self.graph.keys(): return None
        if self.reps: return node.split("-")[0]
        else: return node
    
    def seq_from_path(self, path:list[str])->str or None:
        """
        @brief Gera uma sequência a partir de um caminho no grafo de sobreposição, se o caminho for um caminho hamiltoniano válido.
        @param path caminho no grafo de sobreposição.
        @return A sequência gerada a partir do caminho ou None se o caminho não for válido
        """
        if not self.check_if_hamiltonian_path(path):  #vê se o caminho é hamiltoniano
            return None #se não for dá return None
        seq = self.get_seq(path[0]) #as 3 primeiras letras da seq vão ser as 3 da primeira read do path
        for i in range(1, len(path)):  #por cada i no tamanho do path, iniciado em 1
            prox = self.get_seq(path[i]) #encontra-se a proxima seq no path e vamos buscar apenas a seq, sem o id
            seq += prox[-1] #adiciona à seq apenas a ultima letra, pois as anteriores são prefixos da seq
        return seq    
   
                    
# auxiliary
def composition(k:int, seq:str)->list:
    """
    @brief Função que segmenta em conjuntos de tamanho k
    @param k: kmers
    @para seq: sequência a segmentar
    @return lista de kmers de forma ordenada"""
    res = []
    for x in range(len(seq)-k+1): #por cada x no range do tamanho da seq - k+1
        res.append(seq[x:x+k])
    res.sort()
    return res
    
def suffix (seq:str)->str:
    """
    @brief Função de sufixo, que retorna toda a sequência exceto o primeiro valor
    @return string da sequência exceto o primeiro caractere
    """ 
    return seq[1:]
    
def prefix(seq:str)->str:
    """
    @brief Função de prefixo, que retorna toda a sequência exceto o último valor
    @return string da sequência exceto o último caractere
    """
    return seq[:-1]

  
# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print (composition(k, seq))
   
def test2():
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags, False)
    ovgr.print_graph()

def test3():
     frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
     ovgr = OverlapGraph(frags,True)
     ovgr.print_graph()

def test4():
    frags = ["ATA",  "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA" , "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags,True)
    path = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3']
    print (ovgr.check_if_valid_path(path))
    print (ovgr.check_if_hamiltonian_path(path))
    path2 = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3', 'TGG−13', 'GGC−10', 'GCA−9', 'CAT−6', 'ATT−4', 'TTT−15', 'TTC−14', 'TCA−12', 'CAT−7', 'ATA−1', 'TAA−11']
    print (ovgr.check_if_valid_path(path2))
    print (ovgr.check_if_hamiltonian_path(path2))
    #print (ovgr.seq_from_path(path2))

def test5():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags,True)

    path = ovgr.search_hamiltonian_path()
    print(path)
    print (ovgr.check_if_hamiltonian_path(path))
    print (ovgr.seq_from_path(path))

def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print (frags)
    ovgr = OverlapGraph(frags,True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print (path)
    print (ovgr.seq_from_path(path))
   
if __name__ == "__main__":
    print("Test 1:")
    test1()
    print()
    print("Test 2:")
    test2()
    print()
    print("Test 3:")
    test3()
    print()
    print("Test 4:")
    test4()
    print()
    print("Test 5:")
    test5()
    print()
    print("Test 6:")
    test6()
    print()
    print("DONE")
