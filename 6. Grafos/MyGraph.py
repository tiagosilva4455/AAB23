# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 01:33:42 2017

@author: miguelrocha
"""

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    def __init__(self, g: dict = {}) -> None:
        '''
        @brief Construtor da class MyGraph
        @param g: dicionário para preencher o grafo, onde as keys são os identificadores dos nós e os values os arcos. Por default recebe um dicionário vazio
        '''
        self.graph = g

    def print_graph(self) -> None:
        '''
        @brief Printa o conteúdo do grafo como uma lista adjecente
        '''
        for v in self.graph.keys():  # keys - identificadores dos nós
            print(v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self) -> list[int]:
        '''
        @brief Função que retorna lista dos nós do grafo
        @returns lista dos nós do grafo
        '''
        return list(self.graph.keys())

    def get_edges(self) -> list[tuple]:
        '''
        @brief Função que vai buscar os arcos (edges) no grafo
        @returns arcos (edges) no grafo como uma lista de tuplos (origin, destination)
        '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    def size(self) -> tuple[int]:
        '''
        @brief Função que indica o tamanho do grafo
        @returns tamanho do grafo: números de nós e número de arcos
        '''
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges

    def add_vertex(self, v: int) -> None:
        '''
        @brief Adiciona um vértice ao grafo. Verifica se o vértice existe, e não adiciona caso afirmativo
        @param v: vértice
        '''
        if v not in self.graph.keys():  # pode se omitir o .keys()
            self.graph[v] = []

    def add_edge(self, o: int, d: int) -> None:
        '''
         @brief Adiciona um arco ao grafo. Se os nós o ou d não existirem, são adicionados ao grafo
         @param o: origem
         @param d: destino
         '''
        self.add_vertex(o)
        self.add_vertex(d)
        self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v: int) -> list[int]:
        """
        @brief Função que dá a lista de nós sucessores
        @return Lista dos nós sucessores
        """
        return list(self.graph[v])

    def get_predecessors(self, v: int) -> list[int]:
        """
        @brief Função que dá a lista de nós antecedentes do nó v
        @return lista dos nós antecedentes
        """
        res = []
        for k in self.graph:
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v: int) -> list[int]:
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

    def out_degree(self, v: int) -> int:
        """
        @brief Calcula o grau de saída do nó v
        @return grau de saída do nó v
        """
        return len(self.graph[v])

    def in_degree(self, v: int) -> int:
        """
        @brief Calcula o grau de entrada do nó v
        @return grau de entrada do nó v
        """
        return len(self.get_predecessors[v])

    def degree(self, v: int) -> int:
        """
        @brief Calcula o grau do nó v (todos os nós adjacentes quer percursores quer sucessores)
        @return graus do nó v
        """
        return len(self.get_adjacents(v))
        
    def all_degrees(self, deg_type:str = "inout") -> dict:
        '''
        @brief Calcula os graus de todos os nodos do grafo
        @param deg_type: especifica o tipo de graus a calcular
        @return Os graus de todos os nodos do grafo
        '''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs
    
    def highest_degrees(self, all_deg:dict= None, deg_type:str = "inout", top:int= 10):
        '''
        @brief Retorna a lista dos nodos do topo com o maior grau
        @param all_deg: dicionario de todos os graus
        @param deg_type: tipo de grau
        @param top: numero de nodos a listar
        @return lista dos nodos de topo com maior grau
        '''
        if all_deg is None: 
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_deg[:top]))
        
    
    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"):
        '''
        @brief Calcula o grau médio do grafo
        @param deg_type: tipo de grau
        @return o grau médio do grafo
        '''
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))
        
    def prob_degree(self, deg_type:str = "inout")->dict:
        '''
        @brief Calcula a probabilidade de distribuição dos graus no grafo
        @param deg_type: tipo de graus
        @return dicionario com as probabilidades de ditribuição para um dado grau
        '''
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res    
    
    
    ## BFS and DFS searches    

    def reachable_bfs(self, v: int) -> list[int]:
        """
        @brief Função que implementa nós atingíveis em largura
        @param v: vértice/nó
        @return Lista de nós processados
        """
        l = [v]  # guarda-se o nó origem numa lista, lista de nós a ser processados
        res = []  # nós já processados
        while len(l) > 0:  # enquanto a lista não estiver vazia (len>0)
            node = l.pop(0)
            if node != v: res.append(node)  # guardamos na lista o novo nó, que não é o de origem
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v: int) -> list[int]:
        """
        @brief Função que implementa nós atingíveis em profundidade
        @param v: vértice/nó
        @return Lista de nós processados
        """
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)  # se o novo nó é diferente do no origem vamos adicionar à lista
            s = 0  # inicializar a posição a inserir o nó
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res

    def distance(self, s: int, d: int) -> list[tuple]:
        """
        @brief Função de distância entre os nós s e d
        @param s: nó
        @param d: nó
        @return retorna a distância entre os nós s e d
        """
        if s == d: return 0
        res = [(s, 0)]  # cria uma lista de tuplos entre o nó e a distância
        visitado = [s]  # n´so que já foram visitados
        while len(res) > 0:
            no, dist = res.pop(0)
            for elem in self.graph[no]:  # sucessores do nó
                if elem == d:  # quando vemos que é destino, pomos dist+1 e damos return
                    return dist + 1
                elif elem not in visitado:
                    res.append((elem, dist))  # adicionamos à lista de tuplos
                    visitado.append(elem)  # elem agora está visitado

        return None  # apenas acontece se não for atingível
        
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
        @brief
        """
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res
 
    ## mean distances ignoring unreachable nodes
    def mean_distances(self)-> float:
    '''
    @brief Calcula a distancia media entre todos os pares de nós do grafo
    @return a distancia média e o nodo
    '''
        tot = 0
        num_reachable = 0
        for k in self.graph.keys(): 
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable)/((n-1)*n)  
    
    def closeness_centrality(self, node: str) -> float:
        '''
        @brief Calcula a centralidade de proximidade de um dado nodo
        @param node: nodo
        @return o valor da centralidade de proximidade
        '''
        dist = self.reachable_with_dist(node)
        if len(dist)==0: return 0.0
        s = 0.0
        for d in dist: s += d[1]
        return len(dist) / s
        
    
    def highest_closeness(self, top:int = 10)->list[str]:
        '''
        @brief Calcula qual os nodos com a maior proximidade.
        @param top: numero de nodos a incluir
        @return lista de nodos com a maior proximidade
        '''
        cc = {}
        for k in self.graph.keys():
            cc[k] = self.closeness_centrality(k)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_cl[:top]))
            
    
    def betweenness_centrality(self, node:str)->float:
        '''
        @brief Calcula a centralidade de intermediação de um dado nodo
        @param node: nodo
        @return o valor da centralidade de intermediação
        '''
        total_sp = 0
        sps_with_node = 0
        for s in self.graph.keys(): 
            for t in self.graph.keys(): 
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp: sps_with_node += 1 
        return sps_with_node / total_sp
                    
    
    ## cycles    
    def node_has_cycle (self, v:str)->bool:
        '''
        @brief Verifica se um dado nodo faz parte de um ciclo
        @param v: nodo a verificar
        @return Booleano correspondente se fizer ou nao parte do ciclo
        '''
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
    
    def has_cycle(self)->bool:
        '''
        @brief Verifica se o grafo contem um ciclo
        @return Booleano correspondente se tiver ou nao um ciclo
        '''
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res

    ## clustering
        
    def clustering_coef(self, v:str)->float:
        '''
        @brief Calcula o coeficiente de clustering para um dado nodo
        @param v: nodo a verificar
        @return o valor correspondente ao coeficiente de clustering
        '''
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):
        '''
        @brief Calcula todos os coeficientes de clustering do grafo
        @return um dicionario do valor correspondente ao coeficiente de clustering de cada nodo
        '''
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):
        '''
        @brief Calcula o valor médio do coeficiente de clustering do grafo
        @return o valor médio correspondente ao coeficiente de clustering do grafo
        '''
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type:str = "inout")-> dict:
        '''
        @brief Calcula o valor médio do coeficiente de clustering por nodo com o mesmo grau
        @param deg_type: O tipo de grau a considerar
        @returns Um dicionario que relaciona cada grau com o seu valor médio de coeficiente de clustering
        '''
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys(): degs_k[degs[k]].append(k)
            else: degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

    ## Hamiltonian

    def check_if_valid_path(self, p:list[str])->bool:
        '''
        @brief Verifica se dado caminho é um caminho valido
        @param p: O caminho
        @returns Retorna um booleano dependendo da resposta
        '''
        if p[0] not in self.graph.keys(): return False
        for i in range(1,len(p)):
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i-1]]:
                return False
        return True
        
    def check_if_hamiltonian_path(self, p:list[str])-> bool:
        '''
        @brief Verifica se dado caminho é um caminho hamiltoniano
        @param p: O caminho
        @returns Retorna um booleano dependendo da resposta
        '''
        if not self.check_if_valid_path(p): return False
        to_visit = list(self.get_nodes())
        if len(p) != len(to_visit): return False
        for i in range(len(p)):
            if p[i] in to_visit: to_visit.remove(p[i])
            else: return False
        if not to_visit: return True
        else: return False
    
    def search_hamiltonian_path(self)->list[str]:
        '''
        @brief Procura um caminho hamiltoniano no grafo
        @returns O caminho hamiltoniano no grafo se houver, ou None
        '''
        for ke in self.graph.keys():
            p = self.search_hamiltonian_path_from_node(ke)
            if p != None:
                return p
        return None
    
    def search_hamiltonian_path_from_node(self, start:str)->list[str]:
        '''
        @brief Procura um caminho hamiltoniano no grafo a iniciar num nodo especifico
        @param start: O nodo inicial de procura
        @returns O caminho hamiltoniano no grafo se houver, ou None
        '''
        current = start
        visited = {start:0}
        path = [start]
        while len(path) < len(self.get_nodes()):
            nxt_index = visited[current]
            if len(self.graph[current]) > nxt_index:
                nxtnode = self.graph[current][nxt_index]
                visited[current] += 1
                if nxtnode not in path:
                    path.append(nxtnode)
                    visited[nxtnode] = 0                    
                    current = nxtnode      
            else: 
                if len(path) > 1: 
                    rmvnode = path.pop()
                    del visited[rmvnode]
                    current = path[-1]
                else: return None
        return path

    # Eulerian
    
    def check_balanced_node(self, node:str)->bool:
        '''
        @brief Verifica se um nodo é balanceado, ou seja, se o in-degree é igual ao out-degree
        @param node: o nodo que queremos verificar
        @returns booleano dependendo da resposta
        '''
        return self.in_degree(node) == self.out_degree(node)
        
    def check_balanced_graph(self)->bool:
        '''
        @brief Verifica se o grafo é balanceado, ou seja, se todos os nodos são balanceados
        @returns booleano dependendo da resposta
        '''
        for n in self.graph.keys():
            if not self.check_balanced_node(n): return False
        return True
    
    def check_nearly_balanced_graph(self)->tuple:
        '''
        @brief Verifica se o grafo está proximo de balanceado, ou seja, se todos os nodos são balanceados ou tem um grau de diferença.
        @returns tuplo que contem 2 nodos (primeiro, ultimo), que nao estao balanceados mas têm diferença de 1 no seu grau ou (None, None), caso nao seja balanceado
        '''
        res = None, None
        for n in self.graph.keys():
            indeg= self.in_degree(n)
            outdeg= self.out_degree(n)
            if indeg - outdeg == 1 and res[1] is None: res = res[0], n
            elif indeg - outdeg == -1 and res[0] is None: res = n, res[1]
            elif indeg == outdeg: pass
            else: return None, None 
        return res

    def is_connected(self)->bool:
        """
        @brief Verifica se o grafico está conectado, ou seja, se existe um caminho entre todos os pares de nodos
        @return booleano dependendo da reposta
        """
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys():
            reachable_v = self.reachable_bfs(v)
            if (len(reachable_v) < total): return False
        return True

    def eulerian_cycle(self)->list[str]:
        """
        @brief Encontra um ciclo eulariano, se um existir
        @return O ciclo eulariano, ou None caso não exista
        """
        if not self.is_connected() or not self.check_balanced_graph(): return None
        edges_visit = list(self.get_edges())
        res = []
        while edges_visit:
            pass  ## completar aqui
        return res                 
      
    def eulerian_path(self)->list[str]:
        """
        @brief Encontra um caminho eulariano, se um existir
        @return O caminho eulariano, ou None caso não exista
        """
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None: return None
        self.graph[unb[1]].append(unb[0])
        cycle = self.eulerian_cycle()
        for i in range(len(cycle)-1):
            if cycle[i] == unb[1] and cycle[i+1] ==  unb[0]:
                break
        path = cycle[i+1:] + cycle[1:i+1]
        return path


def is_in_tuple_list(tl:list[tuple], val:any)->bool:
    """
    @brief Verifica se um valor está presente como primeiro elemento de qualquer tuplo dentro de uma dada lista de tuplos.
    @param tl: lista de tuplos a procura
    @param val: valor que se quer encontrar
    @return Um booleano dependendo da resposta
    """
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
    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    
    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
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
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1,2)
    gr.add_edge(2,3)
    gr.add_edge(3,2)
    gr.add_edge(3,4)
    gr.add_edge(4,2)
    gr.print_graph()
    print(gr.size())
    
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    
    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))
    
    gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))
    
    print(gr2.distance(1,7))
    print(gr2.shortest_path(1,7))
    print(gr2.distance(1,8))
    print(gr2.shortest_path(1,8))
    print(gr2.distance(6,1))
    print(gr2.shortest_path(6,1))
    
    print(gr2.reachable_with_dist(1))
    
    print(gr.has_cycle())
    print(gr2.has_cycle())
    
    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))

if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
    #test6()
    
    
