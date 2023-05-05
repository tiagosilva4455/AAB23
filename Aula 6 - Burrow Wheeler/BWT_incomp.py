# -*- coding: utf-8 -*-

class BWT:
    
    def __init__(self, seq = "", buildsufarray = False):
        self.bwt = self.build_bwt(seq, buildsufarray) 
    
    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text:str, buildsufarray:bool = False)->str:
        """
        Retorna a ultima coluna da matriz da BWT
    
        Args:
            text (str): texto de entrada para o qual a BWT será construída.
            buildsufarray (bool, opcional): boolean que indica se o array de sufixos deve ser construído, valor por default é False.

        Returns:
            res (str): a transformada de Burrows-Wheeler do texto de entrada.
        """
        ls = []
        for i in range(len(text)):
            ls.append(text[i:] + text[:i])

        ls.sort()
        res = " "

        for i in range(len(text)):
            res += ls[i][len(text) - 1]

        if buildsufarray:
            self.sa = []
            for i in range(len(ls)):
                stpos = ls[i].index("$")
                self.sa.append(len(text)-stpos-1)

        return res    
    
    def inverse_bwt(self)->str:
        """
        Reverte a transformação de Burrows-Wheeler de forma a obter o texto original.

        Returns:
            res(str): O texto original antes da aplicação da BWT.

        """
        firstcol = self.get_first_col()
        res = ""
        c = "$" 
        occ = 1
        for i in range(len(self.bwt)):
            return res
 
    def get_first_col (self)->list:
        """
            Retorna a primeira coluna do quadro de sufixos, obtida a partir da BWT

            Returns:
                firstcol(list): Uma lista contendo os caracteres da primeira coluna do quadro de sufixos.
        """
        firstcol = []
        for c in self.bwt:
            firstcol.append(c)
            firstcol.sort()
        return firstcol
        
    def last_to_first(self)->list:
        """
            Retorna uma lista contendo os índices da última ocorrência de cada caractere da BWT na primeira coluna do quadro de sufixos.

            Returns:
                res (list) : Uma lista de índices correspondentes à última ocorrência de cada caractere na primeira coluna do quadro de sufixos.
        """
        res = []
        firstcol = self.get_first_col()
        for i in range(len(firstcol)):
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1
            res.append(find_ith_occ(firstcol, c, ocs))
        return res


    def bw_matching(self, patt:str)->list:
        """
        Retorna uma lista de índices correspondentes aos sufixos da BWT que possuem o padrão de busca especificado.

        Args:
            patt (str): O padrão de busca a ser procurado na BWT.

        Returns:
            res (list): Uma lista de índices correspondentes aos sufixos da BWT que possuem o padrão de busca especificado.
        """
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt)-1
        flag = True
        while flag and top <= bottom:
            if patt != "":
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom+1)]
                if symbol in lmat:
                    topIndex = lmat.index(symbol) + top
                    bottomIndex = bottom - lmat[::-1].index(symbol)
                    top = lf[topIndex]
                    bottom = lf[bottomIndex]
                else: flag = False
            else: 
                for i in range(top, bottom+1): res.append(i)
                flag = False            
        return res        
 
    def bw_matching_pos(self, patt:str)-> list:
        """
            Realiza correspondência de padrões utilizando a BWT e retorna as posições dos sufixos correspondentes.

            Args:
                patt (str): O padrão a ser procurado na BWT.

            Returns:
                res(list): Uma lista contendo as posições dos sufixos correspondentes no texto original.


        """
        res = []
        matches = self.bw_matching(patt)
        for m in matches:
            res.append(self.sa[m])
        res.sort()
        return res
 
# auxiliary
 
def find_ith_occ(l, elem, index):
    j, k = 0, 0
    while k < index and j < len(l):
        if l[j] == elem:
            k = k + 1
            if k == index: return j
        j += 1
    return -1


      
def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print (bw.bwt)
#    print (bw.last_to_first())
#    print (bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print (bw.inverse_bwt())

def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
#    print(bw.bw_matching_pos("AGA"))

test()
#test2()
#test3()

