import piece
import utilitaire.constante as cst
import pygame
import utilitaire.fonction_utile as fct
from piece import Reine,Pion
from scene_droite import SceneDroite
from utilitaire.eventhandler import eventhandler
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
        self.coup = []
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



    def generer_piece(self,cla,ind:int,blanc:bool):
        if blanc:
            return cla(ind%8,ind//8,'blanc',self)
        else:
            return cla(ind % 8, ind // 8, 'noir', self)

    def calcul_all_coup(self, couleur, roi_mouv=True, calcul=True, en_passant=True) -> None or list[
        tuple[int]]:
        l = []
        for elem in self.piece_dic[couleur]:
            if elem.piece == 'pion' and elem.peut_jouer:
                elem.calcul_coup(calcul=calcul, detect_enpassent=en_passant)
            elif elem.piece != 'roi' and elem.peut_jouer:
                elem.calcul_coup(calcul=calcul)
            elif elem.piece == 'roi' and roi_mouv and elem.peut_jouer:
                elem.calcul_coup(calcul=calcul)
            l.extend(elem.coup)
        if calcul and couleur == self.couleur_joueur:
            self.coup_couleur[couleur].extend(l)
        return l

    def preparer_couleur_joue(self,couleur):
        for lst in self.coup_couleur.values():
            lst.clear()
        for lst in self.piece_dic.values():
            lst.clear()
        self.mettre_piece_dans_liste()
        self.roi[fct.autre_couleur(couleur)].enlever_echec()
        self.calcul_all_coup(couleur)
        if len(self.coup_couleur[couleur]) == 0:
            self.parti.joueur_gagnant = autre_couleur(self.couleur_joueur)
            eventhandler.activer_event(cst.EVENTMAT)

    def creer_coup(self,piec,destination):
        rock = None
        ep = False
        promote = False
        if piec.piece == "pion":
            promote = destination[1] == 0 or destination[1] == 7
            debut, met_echec, piece_manger,ep = self.check_ep(piec,destination)
        if piec.piece == "roi" and abs(piec.coordone[0]-destination[0]) == 2:
            debut, met_echec, piece_manger,rock = self.coup_met_en_echec_rock(piec,destination)
        elif not ep :
            debut, met_echec, piece_manger = self.coup_met_en_echec(piec,destination)
        return (debut,piec.piece,destination,piece_manger,met_echec,piec.couleur,rock,ep,promote)

    def coup_met_en_echec(self,piec,destination):
        i, j = destination
        debut = piec.coordone
        piece_manger = self.echiquier[i][j]
        met_echec = False
        self.deplacer_piece(piec, destination)
        piec.calcul_coup(calcul=False)
        if self.roi[autre_couleur(piec.couleur)].coordone in piec.coup:
            met_echec = True
        self.deplacer_piece(piec, debut)

        if piece_manger is not None:
            self.echiquier[i][j] = piece_manger
            piece_manger = piece_manger.piece

        return debut,met_echec,piece_manger


    def check_ep(self,piec,destination):
        x,y = piec.coordone
        i,j = destination
        piece_manger = None
        if piec.piece == 'pion' :
            if abs(x - i) == 1 :
                if j-1 >=0 and not self.echiquier[i][j-1] is None and self.echiquier[i][j-1] in self.show_ep() :
                    piece_manger = self.echiquier[i][j - 1]
                elif j+1 <=7 and not self.echiquier[i][j+1] is None and self.echiquier[i][j+1] in self.show_ep() :
                    piece_manger = (self.echiquier[i][j+1])
        ep = piece_manger is not None
        if ep :
            piece_manger = piece_manger.piece
        debut,met_echec,_ = self.coup_met_en_echec(piec,destination)
        return debut,met_echec,piece_manger,ep

    def coup_met_en_echec_rock(self,piec,destination):
        i, j = destination
        rock = "rd" if i > piec.coordone[0] else 'rg'
        debut = 0 if rock == "rg" else 7
        if piec.coordone[1] == 0:
            rock = rock.upper()
        piece_deplacer = self.echiquier[debut][piec.coordone[1]]
        debut = piece_deplacer.coordone
        met_echec = False
        self.deplacer_piece(piece_deplacer, destination)
        piece_deplacer.calcul_coup(calcul=False)
        if self.roi[autre_couleur(piece_deplacer.couleur)].coordone in piece_deplacer.coup:
            met_echec = True
        self.deplacer_piece(piece_deplacer, debut)
        return debut,met_echec,None,rock

    def deplacer_piece(self,piec,destination,vraiment=False):
        x,y = piec.coordone
        self.echiquier[x][y] = None
        i, j = destination
        piec.changer_pos(destination)
        self.echiquier[i][j] = piec
        if vraiment:
            piec.premier_coup = False

    def jouer_rock(self,rock:str,vraiment=False):
        y = 7 if rock.islower() else 0
        x = 7 if rock[1].lower() == 'd' else 0
        i1 = 5 if x == 7 else 3
        i2 = 6 if x == 7 else 2
        self.deplacer_piece(self.echiquier[x][y],(i1,y),vraiment)
        self.deplacer_piece(self.echiquier[4][y], (i2, y), vraiment)

    def dejouer_rock(self,rock:str):
        y = 7 if rock.islower() else 0
        x = 7 if rock[1].lower() == 'd' else 0
        i1 = 5 if x == 7 else 3
        i2 = 6 if x == 7 else 2
        self.deplacer_piece(self.echiquier[i1][y], (x, y))
        self.deplacer_piece(self.echiquier[i2][y], (5, y))

    def jouer_coup(self,coup,vraiment=True):
        self.ep.clear()
        co_piece_bouger, piece_bouger, destination ,piece_manger,met_echec,couleur,rock,ep,promote = coup
        if rock is None :
            x,y = co_piece_bouger
            piec = self.echiquier[x][y]
            self.deplacer_piece(piec,destination,True)
        else:
            self.jouer_rock(rock,vraiment)
        if piece_bouger == "pion" and abs(co_piece_bouger[1] - destination[1]) == 2 :
            self.ep.append(self.echiquier[destination[0]][destination[1]])
        if ep :
            self.echiquier[destination[0]][co_piece_bouger[1]] = None
        if promote :
            i,j = destination
            self.echiquier[i][j] = Reine(i,j,couleur,self)
        if met_echec:
            self.roi[autre_couleur(couleur)].roi_echec()
        if vraiment :
            self.scene_droite.ajouter_coup(coup)
            self.coup.append(coup)

    def dejouer_coup(self,coup):
        co_piece_bouger, piece_bouger, destination, piece_manger, met_echec, couleur, rock, ep, promote = coup
        dic_fr_en = {'p':'p','c':'c','f':'b','d':'q','r':'k','t':'r'}
        self.ep.clear()
        if rock is not None :
            self.dejouer_rock(rock)
            return
        x,y = destination
        self.deplacer_piece(self.echiquier[x][y],co_piece_bouger)
        if ep :
            if couleur == 'blanc' :
                self.echiquier[x][y+1] = Pion(x,y+1,'noir',self)
            else:
                self.echiquier[x][y-1] = Pion(x, y - 1, 'blanc', self)
            return
        piec = self.generer_piece(self.piece_dic[dic_fr_en[piece_manger[0]]],x+y*8,couleur == 'noir')
        self.echiquier[x][y] = piec





