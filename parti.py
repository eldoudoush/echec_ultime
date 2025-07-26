from echiquier import Echiquier
import utilitaire.constante as cst
import utilitaire.fonction_utile as fct
import pygame

from utilitaire.fonction_utile import autre_couleur


# un coup est : [coordone de la piece bouger , piece bouger , coordone d'arriver ,
#               piece manger si une piece est manger sinon None, met_echec:bool,couleur de la piece bouger]

class Parti:
    def __init__(self):
        self.echiquier = Echiquier(self)
        self.piece_selectione = None
        self.parti_en_cour = True
        self.preview = []
        self.piece_mort = {"blanc":[],"noir":[]}
        self.joueur_gagnant = None
        self.coup_jouer = []

    def afficher(self,surface):
        if not self.parti_en_cour :
            return
        self.echiquier.afficher_case()

        for image in self.preview :
            image.afficher(surface)

        self.echiquier.afficher_piece(surface)

    def click(self):
        if not self.parti_en_cour:
            return
        x,y = pygame.mouse.get_pos()
        x = int( x // cst.taille_case)
        y = int( y // cst.taille_case)
        if not fct.out_of_board((x,y)):
            return

        if self.echiquier.echiquier[x][y] is not None and self.echiquier.echiquier[x][y].couleur == self.echiquier.couleur_joueur:
            print(self.echiquier.echiquier[x][y].coup)
            self.changer_piece_selectione(self.echiquier.echiquier[x][y])
        elif not self.piece_selectione is None and (x,y) in self.piece_selectione.coup :
            self.deplacer_piece(self.piece_selectione,(x,y))
            self.changer_piece_selectione(None)
        else:
            self.changer_piece_selectione(None)

    def tour_suivant(self):
        if self.echiquier.roi_noir.roi_en_echec :
            self.echiquier.roi_noir.actualiser_image()
            self.echiquier.roi_noir.roi_en_echec = False
        elif self.echiquier.roi_blanc.roi_en_echec :
            self.echiquier.roi_blanc.actualiser_image()
            self.echiquier.roi_blanc.roi_en_echec = False

        if self.echiquier.couleur_joueur == 'blanc' :
            coup = piece.calcul_coup_noir(self.echiquier)
            coup_ennemi = piece.calcul_coup_blanc(self.echiquier,calcul=False)
            self.couleur_joueur = 'noir'
            if len(coup) == 0:
                self.parti_en_cour = False
                self.joueur_gagnant = 'blanc'
            elif self.echiquier.roi_noir.coordone in coup_ennemi :
                self.echiquier.roi_noir.roi_echec()

        else :
            coup = piece.calcul_coup_blanc(self.echiquier)
            coup_ennemi = piece.calcul_coup_noir(self.echiquier, calcul=False)
            self.couleur_joueur = 'blanc'
            if len(coup) == 0:
                self.parti_en_cour = False
                self.joueur_gagnant = 'blanc'
            elif self.echiquier.roi_noir.coordone in coup_ennemi:
                self.echiquier.roi_noir.roi_echec()

    def changer_piece_selectione(self,piece):
        self.preview.clear()
        self.piece_selectione = piece
        if piece is None:
            return
        self.creer_preview()


    def creer_preview(self):
        self.preview.clear()
        tc = cst.taille_case
        for elem in self.piece_selectione.coup :
            x,y = elem
            if self.echiquier.echiquier[x][y] is None :
                self.preview.append(fct.Image(pygame.Rect(tc*x,tc*y,tc,tc),"image/point/point_grisv2.png"))
            else:
                self.preview.append(fct.Image(pygame.Rect(tc*x,tc*y,tc,tc),"image/point/point_rougev2.png"))
        x,y = self.piece_selectione.coordone
        self.preview.append(fct.Image(pygame.Rect(tc*x,tc*y,tc,tc),"image/point/selectione.png"))

    def jouer_coup(self,piece,destination):
        x,y = destination
        piece_capture = None if self.echiquier.echiquier[x][y] is None else self.echiquier.echiquier[x][y].piece

        coup = (piece.coordone,piece.piece,destination,piece_capture)

    def deplacer_piece(self,piece ,coordone):
        piece.premier_coup = False
        x,y = piece.coordone
        i,j = coordone
        destination = self.echiquier.echiquier[i][j]
        self.echiquier.echiquier[x][y] = None
        if not destination is None :
            self.piece_prise(destination)

        if piece.piece == 'pion' :
            if abs(x - i) == 1 :
                if j-1 >=0 and not self.echiquier.echiquier[i][j-1] is None and self.echiquier.echiquier[i][j-1] in self.echiquier.show_ep() :
                    self.piece_prise(self.echiquier.echiquier[i][j - 1])
                    self.echiquier.echiquier[i][j - 1] = None
                elif j+1 >=7 and not self.echiquier.echiquier[i][j+1] is None and self.echiquier.echiquier[i][j+1] in self.echiquier.show_ep() :
                    self.piece_prise(self.echiquier.echiquier[i][j+1])
                    self.echiquier.echiquier[i][j + 1] = None
        self.echiquier.ep.clear()
        if piece.piece == 'pion' and abs(piece.coordone[1] - j) == 2 :
            self.echiquier.ep.append(piece)

        self.echiquier.echiquier[i][j] = piece
        piece.coordone = (i,j)
        piece.actualiser_image()
        if piece.piece == 'pion' and piece.coordone[1] in [0,7]:
            reine = Reine(i, j, piece.couleur,self.echiquier)
            self.piece_prise(piece,False)
            if piece.couleur == 'blanc':
                self.echiquier.piece_blanc.append(reine)
            else:
                self.echiquier.piece_noir.append(reine)
            self.echiquier.echiquier[i][j] = reine

    def piece_prise(self,piece,mort=True):
        if mort :
            self.piece_mort[piece.couleur].append(piece)
            piece.mort = True
        if piece.couleur == 'blanc':
            self.echiquier.piece_blanc.remove(piece)
        else:
            self.echiquier.piece_noir.remove(piece)

    def boucle(self):
        self.echiquier.boucle()

class PartiLocal(Parti):
    def __init__(self):
        super().__init__()
        self.echiquier.preparer_couleur_joue(self.echiquier.couleur_joueur)

    def deplacer_piece(self,piece,destination):
        coup = self.echiquier.creer_coup(piece,destination)
        self.echiquier.jouer_coup(coup)
        self.echiquier.couleur_joueur = autre_couleur(self.echiquier.couleur_joueur)
        self.echiquier.preparer_couleur_joue(self.echiquier.couleur_joueur)
