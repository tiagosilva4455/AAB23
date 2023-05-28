# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class OverlapGraph(MyGraph):
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_overlap_graph(frags)

#    def __init__(self, frags, reps = False):
#        if reps: self.create_overlap_graph_with_reps(frags)
#        else: self.create_overlap_graph(frags)
#        self.reps = reps
        
    
    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags):
        for x in frags: #por sequencia em frag
            self.add_vertex(x)  #cria vértice no grafo
        for seq in frags:
                sufixo = suffix(seq)  #verifica qual é o sufixo da seq, ou seja todas as letras exceto a primeira da seq
                for seq2 in frags:
                    if prefix(seq2) == sufixo: #se o prefixo, ou seja tudo menos a ultima letra, é igual ao sufixo
                        self.add_edge(seq,seq2) #adiciona um edge que é um tuplo  (sufixo,prefixo)

        
    def create_overlap_graph_with_reps(self, frags):  # caso de replicas de fragmentos
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
    
    def get_instances(self, seq):
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res
    
    def get_seq(self, node):
        if node not in self.graph.keys(): return None
        if self.reps: return node.split("-")[0]
        else: return node
    
    def seq_from_path(self, path):
        # ...
        return seq    
   
                    
# auxiliary
def composition(k, seq):
    res = []
    #...
    return res
    
def suffix (seq): 
    return seq[1:]
    
def prefix(seq):
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
     ovgr = OverlapGraph(frags, True)
     ovgr.print_graph()

def test4():
    frags = ["ATA",  "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA" , "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    path = [’ACC−2’, ’CCA−8’, ’CAT−5’, ’ATG−3’]
    print (ovgr.check_if_valid_path(path))
    print (ovgr.check_if_hamiltonian_path(path))
    path2 = [’ACC−2’, ’CCA−8’, ’CAT−5’, ’ATG−3’, ’TGG−13’, ’GGC−10’, ’GCA−9’, ’CAT−6’, ’ATT−4’, ’TTT−15’, ’TTC−14’, ’TCA−12’, ’CAT−7’, ’ATA−1’, ’TAA−11’]
    print (ovgr.check_if_valid_path(path2))
    print (ovgr.check_if_hamiltonian_path(path2))
    #print (ovgr.seq_from_path(path2))

def test5():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)

    path = ovgr.search_hamiltonian_path()
    print(path)
    print (ovgr.check_if_hamiltonian_path(path))
    print (ovgr.seq_from_path(path))

def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print (frags)
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print (path)
    print (ovgr.seq_from_path(path))
   
test1()
print()
test2()
print()
#test3()
#print()
#test4()
#print()
#test5()
#print()
#test6()
