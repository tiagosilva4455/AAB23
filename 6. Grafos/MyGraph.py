# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    """
    Implementação de uma classe para representar grafos orientados
    """
    
    def __init__(self, g:dict = {})->None:
        ''' 
        @brief Construtor da class MyGraph
        @param g: dicionário para preencher o grafo, onde as keys são os identificadores dos nós e os values os arcos. Por default recebe um dicionário vazio
        '''
        self.graph = g    

    def print_graph(self)->None:
        ''' 
        @brief Printa o conteúdo do grafo como uma lista adjecente
        '''
        for v in self.graph.keys():  #keys - identificadores dos nós
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self)->list[int]:
        ''' 
        @brief Função que retorna lista dos nós do grafo
        @returns lista dos nós do grafo
        '''
        return list(self.graph.keys())
        
    def get_edges(self)->list[tuple]: 
        '''
        @brief Função que vai buscar os arcos (edges) no grafo
        @returns arcos (edges) no grafo como uma lista de tuplos (origin, destination)
        '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
      
    def size(self)->tuple[int]:
        '''
        @brief Função que indica o tamanho do grafo
        @returns tamanho do grafo: números de nós e número de arcos
        '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v:int)->None:
        ''' 
        @brief Adiciona um vértice ao grafo. Verifica se o vértice existe, e não adiciona caso afirmativo
        @param v: vértice
        '''
        if v not in self.graph.keys(): #pode se omitir o .keys()
            self.graph[v]=[]
        
    def add_edge(self, o:int, d:int)->None:
        '''
         @brief Adiciona um arco ao grafo. Se os nós o ou d não existirem, são adicionados ao grafo
         @param o: origem
         @param d: destino
         ''' 
        self.add_vertex(o)
        self.add_vertex(d)
        self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v:int)->list[int]:
        """
        @brief Função que dá a lista de nós sucessores
        @return Lista dos nós sucessores
        """
        return list(self.graph[v])
             
    def get_predecessors(self, v:int)->list[int]:
        """
        @brief Função que dá a lista de nós antecedentes do nó v
        @return lista dos nós antecedentes
        """
        res=[]
        for k in self.graph:
            if v in self.graph[k]:
                res.append(k)
        return res
    
    def get_adjacents(self, v:int)->list[int]:
        """
        @brief Função que dá a lista de nós adjacentes do nó v
        @return lista dos nós adjacentes
        """
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res
        
    ## degrees - número de ligações que ligam esse nó a outros nós (i.e. nº de nós adjacentes)
    
    def out_degree(self, v:int)->int:
        """
        @brief Calcula o grau de saída do nó v
        @return grau de saída do nó v
        """
        return len(self.graph[v])
    
    def in_degree(self, v:int)->int:
        """
        @brief Calcula o grau de entrada do nó v
        @return grau de entrada do nó v
        """
        return len(self.get_predecessors[v])
        
    def degree(self, v:int)->int:
        """
        @brief Calcula o grau do nó v (todos os nós adjacentes quer percursores quer sucessores)
        @return graus do nó v
        """
        return len(self.get_adjacents(v))
    
    # BFS (Breadth First) and DFS (Depth First) searches
    # Existe tambem o interative deepening que nos dá o melhor dos dois mundos porem é menos eficiente

    
    def reachable_bfs(self, v:int)->list[int]:
        """
        @brief Função que implementa nós atingíveis em largura
        @param v: vértice/nó
        @return Lista de nós processados
        """
        l = [v]  #guarda-se o nó origem numa lista, lista de nós a ser processados
        res = []  #nós já processados
        while len(l) > 0:  #enquanto a lista não estiver vazia (len>0)
            node = l.pop(0)
            if node != v: res.append(node)  #guardamos na lista o novo nó, que não é o de origem
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v:int)->list[int]:
        """
        @brief Função que implementa nós atingíveis em profundidade
        @param v: vértice/nó
        @return Lista de nós processados
        """
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)  #se o novo nó é diferente do no origem vamos adicionar à lista
            s = 0 #inicializar a posição a inserir o nó
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s:int, d:int)->list[tuple]:
        """
        @brief Função de distância entre os nós s e d
        @param s: nó
        @param d: nó
        @return retorna a distância entre os nós s e d
        """
        if s == d: return 0
        res = [(s,0)] #cria uma lista de tuplos entre o nó e a distância
        visitado = [s] #n´so que já foram visitados
        while len(res) > 0:
            no, dist = res.pop(0)
            for elem in self.graph[no]: #sucessores do nó
                if elem == d: #quando vemos que é destino, pomos dist+1 e damos return
                    return dist+1
                elif elem not in visitado:
                    res.append((elem, dist)) #adicionamos à lista de tuplos 
                    visitado.append(elem) #elem agora está visitado

        return None  #apenas acontece se não for atingível
        
    def shortest_path(self, s:int, d:int)->None:
        """
        @brief Função de caminho mais curto entre os nós s e d
        @param s: nó
        @param d: nó
        """
        if s == d: return [s,d]
        l = [(s,[])] #guarda-se apenas o antecessor do nó
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return preds+[node, elem]
                elif elem not in visited:
                    l.append((elem, preds+[node]))
                    visited.append(elem)
        return None
        
    def reachable_with_dist(self, s:int)->list[int]:
        """
        @brief """
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())

def test6():
    g = MyGraph()
    g.add_vertex(1)
    print(g.graph)

if __name__ == "__main__":
    test6()
