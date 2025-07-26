import piece
import utilitaire.constante as cst
import pygame
import utilitaire.fonction_utile as fct
from scene_droite import SceneDroite
from utilitaire.fonction_utile import autre_couleur


class Echiquier:
    def __init__(self,parti):
        self.echiquier = [[None for _ in range(8)] for __ in range(8)] #initialise les 64 cases
        self.piece_dic = {"blanc":[],"noir":[]}
        self.roi = {'blanc':None,'noir':None}
        self.couleur_joueur = 'blanc'
        self.ep = []
        self.dic_lettre_piece = {'p':piece.Pion,'c':piece.Cheval,'b':piece.Fou,'r':piece.Tour,'q':piece.Reine,'k':piece.Roi}
        self.init_echiquier(cst.plateau_classique)
        self.coup_couleur = {"blanc":[],"noir":[]}
        self.scene_droite = SceneDroite(self)
        self.parti = parti

    def afficher_case(self):
        tc = cst.taille_case
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    couleur = cst.couleur_case_blanche
                else:
                    couleur = cst.couleur_case_fonce
                pygame.draw.rect(cst.screen, couleur, [tc * i, tc * j, tc, tc])

    def afficher_piece(self,surface):
        for i in range(8):
            for j in range(8):
                if not self.echiquier[i][j] is None:
                    self.echiquier[i][j].afficher(surface)
        self.scene_droite.afficher(surface)

    def show_ep(self):
        return self.ep

    def mettre_piece_dans_liste(self):
        for i in range(8):
            for j in range(8) :
                piece = self.echiquier[i][j]
                if not piece is None :
                    self.piece_dic[piece.couleur].append(piece)

    def init_echiquier(self,plateau:str):
        lst = plateau.split('/')
        ind = 0
        for elem in lst :
            for lettre in elem :
                if lettre.isnumeric() :
                    num = int(lettre)
                    ind += num
                else :
                    piece = self.generer_piece(self.dic_lettre_piece[lettre.lower()],ind,lettre.islower())
                    self.echiquier[ind%8][ind//8] = piece
                    if piece.piece == 'roi' :
                        self.roi[piece.couleur] = piece
                    ind += 1



    def generer_piece(self,cla,ind:int,check:bool):
        if check:
            return cla(ind%8,ind//8,'blanc',self)
        else:
            return cla(ind % 8, ind // 8, 'noir', self)

    def calcul_coup(self, couleur, roi_mouv=True, calcul=True, en_passant=True) -> None or list[
        tuple[int]]:
        l = []
        for elem in self.piece_dic[couleur]:
            if elem.piece == 'pion' and elem.peut_jouer:
                elem.calcul_coup(calcul=calcul, detect_enpassent=en_passant)
            if elem.piece != 'roi' and elem.peut_jouer:
                elem.calcul_coup(calcul=calcul)
                l += elem.coup
            elif elem.piece == 'roi' and roi_mouv and elem.peut_jouer:
                elem.calcul_coup(calcul=calcul)
                l += elem.coup
        if calcul:
            self.coup_couleur[couleur] += l
        return l

    def preparer_couleur_joue(self,couleur):
        self.mettre_piece_dans_liste()
        self.roi[fct.autre_couleur(couleur)].enlever_echec()
        mat = False
        self.calcul_coup(couleur)
        if len(self.coup_couleur[couleur]) == 0:
            mat = True
        return mat

    def creer_coup(self,piec,destination):
        i,j = destination
        debut = piec.coordone
        piece_manger = self.echiquier[i][j]
        met_echec = False
        self.deplacer_piece(piec,destination)
        piec.calcul_coup(calcul=False)
        if self.roi[autre_couleur(piec.couleur)].coordone in piec.coup:
            met_echec = True
        if piece_manger is not None:
            self.echiquier[i][j] = piece_manger
            piece_manger = piece_manger.piece
        self.deplacer_piece(piec, debut)
        return (debut,piec.piece,destination,piece_manger,met_echec,piec.couleur)


    def deplacer_piece(self,piec,destination,vraiment=False):
        x,y = piec.coordone
        self.echiquier[x][y] = None
        i, j = destination
        piec.changer_pos(destination)
        self.echiquier[i][j] = piec
        if vraiment:
            piec.premier_coup = False



    def jouer_coup(self,coup):
        co_piece_bouger, piece_bouger, destination ,piece_manger,met_echec,couleur = coup
        x,y = co_piece_bouger
        piec = self.echiquier[x][y]
        i,j = destination
        self.echiquier[i][j] = piec
        self.deplacer_piece(piec,destination,True)
        if met_echec:
            self.roi[autre_couleur(couleur)].roi_echec()

    def boucle(self):
        if fct.check_event(cst.PASSESECOND):
            self.scene_droite.temp_timer_reduction()


