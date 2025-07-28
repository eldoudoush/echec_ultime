from time import sleep

from echiquier import Echiquier
import utilitaire.constante as cst
import utilitaire.fonction_utile as fct
import pygame
from utilitaire.eventhandler import eventhandler
from utilitaire.fonction_utile import autre_couleur, AffichageBouttonTexteImage


# un coup est : [0 coordone de la piece bouger ,1 piece bouger ,2 coordone d'arriver ,
#               3 piece manger si une piece est manger sinon None,4 met_echec:bool,5 couleur de la piece bouger
#               6 rock : None si pas rock sinon lower pour blanc et g pour gauche les inverse pour le reste
#               7 ep,8 promote]

class Parti:
    def __init__(self):
        self.echiquier = Echiquier(self)
        self.piece_selectione = None
        self.parti_en_cour = True
        self.preview = []
        self.piece_mort = {"blanc":[],"noir":[]}
        self.joueur_gagnant = " error "
        self.coup_jouer = []
        eventhandler.ajouter_event(cst.EVENTMOUSECLICK,self.click)
        eventhandler.ajouter_event(cst.EVENTMAT,self.gerer_mat)
        self.ecran_fin = AffichageBouttonTexteImage("ecran_fin",pygame.rect.Rect(0,0,cst.width,cst.height),active=False)
        self.ecran_fin.add_boutton("retour_menu",(0.25,0.575),(0.5,0.25),texte='retour au menu',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTRETOURAUMENUSOLO,pourcentage=True)
        self.mat = False

    def afficher(self,surface):
        if not self.parti_en_cour :
            return
        self.echiquier.afficher_case()
        for image in self.preview :
            image.afficher(surface)

        self.echiquier.afficher_piece(surface)
        self.ecran_fin.afficher(surface)

    def click(self):
        if not self.parti_en_cour or self.mat:
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

    def gerer_mat(self):
        self.mat = True
        self.ecran_fin.add_texte("texte_gagnant",cst.MOYENNEPOLICE,"le joueur "+self.joueur_gagnant+" a gagner",(0.5,0.3),color="red",iscentre=True,pourcentage=True)
        self.ecran_fin.activer_desactiver(mettre=True)

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
                self.preview.append(fct.Image(None,"gris",pygame.Rect(tc*x,tc*y,tc,tc),"image/point/point_grisv2.png"))
            else:
                self.preview.append(fct.Image(None,"rouge",pygame.Rect(tc*x,tc*y,tc,tc),"image/point/point_rougev2.png"))
        x,y = self.piece_selectione.coordone
        self.preview.append(fct.Image(None,"selectione",pygame.Rect(tc*x,tc*y,tc,tc),"image/point/selectione.png"))

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

class PartiLocal(Parti):
    def __init__(self):
        super().__init__()
        self.echiquier.preparer_couleur_joue(self.echiquier.couleur_joueur)

    def deplacer_piece(self,piece,destination):
        coup = self.echiquier.creer_coup(piece,destination)
        self.echiquier.jouer_coup(coup)
        self.echiquier.couleur_joueur = autre_couleur(self.echiquier.couleur_joueur)
        self.echiquier.preparer_couleur_joue(self.echiquier.couleur_joueur)
