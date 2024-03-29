# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class MetabolicNetwork (MyGraph):
    """
    Implementação da class MetabolicNetwork, sub-classe da class MyGraph, que herda todos os seus atributos e métodos
    """
    
    def __init__(self, network_type:str = "metabolite-reaction", split_rev:bool = False)->None:
        """
        @brief Construtor da class MetabolicNetwork
        @param network_type: indica o tipo de network, e recebe o valor 'metabolite-reaction' por default
        @param split_rev: flag para dar split às reações, recebe por default o booleano False
        """
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = {}
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []
            self.node_types["reaction"] = []
        self.split_rev =  split_rev
    
    def add_vertex_type(self, v:str, nodetype:str)->None:
        """
        @brief Adiciona um vértice com um tipo específico ao grafo
        @param v: vértice
        @param nodetype: indica o tipo de nodo
        """
        self.add_vertex(v)
        self.node_types[nodetype].append(v)
    
    def get_nodes_type(self, node_type:str)->None or list[str]:
        """
        @brief Retorna uma lista com os tipo de nodos
        @param: node_type: indica o tipo de nodos
        @return Lista com os tipo de nodos
        """
        if node_type in self.node_types:
            return self.node_types[node_type]
        else: return None
    
    def load_from_file(self, filename:str)->None:
        """
        @brief Carrega a rede metabólica a partir de um ficheiro
        @param filename: nome do ficheiro
        """
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: raise Exception("Invalid line:")    

        
        if self.net_type == "metabolite-reaction": 
            self.graph = gmr.graph
            self.node_types = gmr.node_types
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr)
        elif self.net_type == "reaction-reaction": 
            self.convert_reaction_graph(gmr)
        else: self.graph = {}
        
        
    def convert_metabolite_net(self, gmr:"MetabolicNetWork")->None:
        """
        @brief Converte a rede metabolica
        @param gmr: rede metabolica a converter
        """
        for m in gmr.node_types["metabolite"]:
            self.add_vertex(m)
            sucessor = gmr.get_successors(m)
            for r in sucessor:
                suc_reaction = gmr.get_successors(r)
                for mm in suc_reaction:
                    if m != mm:
                        self.add_edge(m, mm)
            

        
    def convert_reaction_graph(self, gmr:"MetabolicNetWork")->None: 
        """
        @brief Converte a reação para grafo
        @param gmr: reação a converter
        """
        for r in gmr.node_types["reaction"]:
            self.add_vertex(r)
            suc_reaction = gmr.get_successors(r)  #vai buscar os sucessores, que são os metabolitos
            for m in suc_reaction: #por cada metabolito
                suc_metabolite = gmr.get_successors(m) #ir buscar os sucessores que são as segundas reações
                for rr in suc_metabolite:  #cada segunda reação
                    if r != rr:  #se uma das reações for diferentes da reaçõa inicial
                        self.add_edge(r, rr) #adicionamos um novo edge


def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1","reaction")
    m.add_vertex_type("R2","reaction")
    m.add_vertex_type("R3","reaction")
    m.add_vertex_type("M1","metabolite")
    m.add_vertex_type("M2","metabolite")
    m.add_vertex_type("M3","metabolite")
    m.add_vertex_type("M4","metabolite")
    m.add_vertex_type("M5","metabolite")
    m.add_vertex_type("M6","metabolite")
    m.add_edge("M1","R1")
    m.add_edge("M2","R1")
    m.add_edge("R1","M3")
    m.add_edge("R1","M4")
    m.add_edge("M4","R2")
    m.add_edge("M6","R2")
    m.add_edge("R2","M3")
    m.add_edge("M4","R3")
    m.add_edge("M5","R3")
    m.add_edge("R3","M6")
    m.add_edge("R3","M4")
    m.add_edge("R3","M5")
    m.add_edge("M6","R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction") )
    print("Metabolites: ", m.get_nodes_type("metabolite") )

        
def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("6. Grafos/example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("6. Grafos/example-net.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("6. Grafos/example-net.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("6. Grafos/example-net.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("6. Grafos/example-net.txt")
    rrsn.print_graph()
    print()

  

if __name__ == "__main__":
    print("Test 1:")
    test1()
    print()
    print("Test 2:")
    test2()
    print()
    print("DONE")
