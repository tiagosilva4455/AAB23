# -*- coding: utf-8 -*-

class BWT:
    """
    Implementação da Transformação de Burrows-Wheeler"""
    
    def __init__(self, seq:str = "", buildsufarray:bool = False)->None:
        """
        @brief Construtor da class BWT
        @param seq: sequência a inserir, que toma valor "" se não for inserida
        @param buildsufarray: parâmetro booleano que controla se o sufixo da matriz deve ser construído com a transformação BWT
        """
        self.bwt = self.build_bwt(seq, buildsufarray) 
    
    def set_bwt(self, bw:str)->None:
        """
        @brief Atualiza a sequência BWT com o valor passado como entrada
        @param bw: sequência BWT a ser definida
        """
        self.bwt = bw

    def build_bwt(self, text:str, buildsufarray:bool = False)->str:
        """
        @brief Constrói a transformada de Burrows-Wheeler da sequência "text"
        @param text: sequência de entrada para a construção da BWT
        @param buildsufarray: Booleano para indicar se deve construir também o array de sufixos
        @return A sequência BWT gerada a partir da sequência de entrada "text"
        """
        ls = []
        for i in range(len(text)):
            ls.append(text[i:] + text[:i]) #cria uma lista com as rotações do texto

        ls.sort() #ordena-as
        res = ""

        for i in range(len(text)):
            res += ls[i][len(text) - 1] #constroi a transformada de BW juntando o último caracter de cada rotação circular

        if buildsufarray: #se buildsufarray for True, constroi o array de sufixos correspondente
            self.sa = []
            for i in range(len(ls)):
                stpos = ls[i].index("$") #cncontra a posição do caractere especial '$' na rotação correspondente
                self.sa.append(len(text)-stpos-1) #adiciona o índice do sufixo à lista de índices de sufixos correspondentes

        return res    
    
    def inverse_bwt(self)->str:  #TEMOS QUE 
        """
        @brief Função que retorna a sequência original a partir da transformada de Burrows-Wheeler inversa
        @return A sequência original correspondente à transformada de Burrows-Wheeler armazenada
        """
        firstcol = self.get_first_col()
        res = ""
        c = "$" #caracter inicial, de acordo com a especificação de BWT
        occ = 1 # número de ocorrências do caractere inicial
        for i in range(len(self.bwt)):   #iteramos a partir da última coluna da BWT até obtermos toda a sequência original
            pos = find_ith_occ(self.bwt, c, occ)
            c = firstcol[pos] #atualizamos o caractere c para o próximo da sequência
            occ = 1 
            k = pos-1 #exploramos as ocorrências anteriores do caractere c na coluna
            while firstcol[k] == c and k >= 0: 
                occ += 1
                k -= 1
            res += c 
        return res
 
    def get_first_col (self)->list[str]:
        """
        @brief Retorna a primeira coluna do quadro de sufixos, obtida a partir da BWT
        @return Lista contendo os caracteres da primeira coluna do quadro de sufixos
        """
        firstcol = []
        for c in self.bwt:
            firstcol.append(c)
            firstcol.sort()
        return firstcol
        
    def last_to_first(self)->list[int]:
        """
        @brief Retorna uma lista contendo os índices da última ocorrência de cada caractere da BWT na primeira coluna do quadro de sufixos
        @return Lista de índices correspondentes à última ocorrência de cada caractere na primeira coluna do quadro de sufixos
        """
        res = []
        firstcol = self.get_first_col()
        for i in range(len(firstcol)):
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1 #número de ocorrências de c até à posição i na BWT
            res.append(find_ith_occ(firstcol, c, ocs))
        return res


    def bw_matching(self, patt:str)->list[int]:
        """
        @brief Retorna uma lista de índices correspondentes aos sufixos da BWT que possuem o padrão de busca especificado
        @param patt: O padrão de busca a ser procurado na BWT
        @return Lista de índices correspondentes aos sufixos da BWT que possuem o padrão de busca especificado
        """
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt)-1
        flag = True
        while flag and top <= bottom: #enquanto houver ocorrência do padrão e o índice top for menor ou igual a bottom
            if patt != "":
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom+1)]
                if symbol in lmat: #se o símbolo procurado estiver na porção do vetor, atualiza os índices top e bottom de acordo com a last-to-first
                    topIndex = lmat.index(symbol) + top
                    bottomIndex = bottom - lmat[::-1].index(symbol)
                    top = lf[topIndex]
                    bottom = lf[bottomIndex]
                else: flag = False #
            else: #se o padrão estiver vazio, adiciona os indices entre top e bottom à lista de ocorrências
                for i in range(top, bottom+1): res.append(i)
                flag = False            
        return res        
 
    def bw_matching_pos(self, patt:str)-> list[int]:
        """
        @briefRealiza correspondência de padrões utilizando a BWT e retorna as posições dos sufixos correspondentes
        @param patt: O padrão a ser procurado na BWT
        @returns Lista contendo as posições dos sufixos correspondentes no texto original
        """
        res = []
        matches = self.bw_matching(patt)
        for m in matches:
            res.append(self.sa[m])
        res.sort()
        return res
 
# auxiliary
 
def find_ith_occ(l:list[str], elem:str, index:int)->int:
    """
    @brief Retorna o índice da i-ésima ocorrência do elemento elem na lista l
    @param l: Lista de elementos a ser pesquisada
    @param elem : Elemento a ser pesquisado na lista
    @param index : Índice da ocorrência do elemento a ser retornado
    @return O índice da index-ésima ocorrência do elemento elem na lista l ou -1 se não houver index ocorrências do elemento na lista
    """
    j, k = 0, 0
    while k < index and j < len(l):
        if l[j] == elem:
            k = k + 1
            if k == index: return j
        j += 1
    return -1
