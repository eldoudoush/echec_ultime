import json
from time import sleep
import string
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
    def __init__(self,game):
        self.echiquier = Echiquier(self)
        self.piece_selectione = None
        self.parti_en_cour = True
        self.preview = []
        self.piece_mort = {"blanc":[],"noir":[]}
        self.joueur_gagnant = " error "
        eventhandler.ajouter_event(cst.EVENTMOUSECLICK,self.click)
        eventhandler.ajouter_event(cst.EVENTMAT,self.gerer_mat)
        self.ecran_fin = AffichageBouttonTexteImage("ecran_fin",pygame.rect.Rect(0.15*cst.width,0.15*cst.height,0.7*cst.width,0.7*cst.height),active=False,couleur_bg=(50,50,50))
        self.ecran_fin.add_boutton("retour_menu",(0.25,0.6),(0.5,0.25),texte='retour au menu',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTRETOURAUMENUSOLO,pourcentage=True)
        self.ecran_fin.add_texte("texte_save",cst.TRESPETITEPOLICE,"nommer la sauvgarde :",(0.5,0.25),iscentre=True,pourcentage=True)
        self.ecran_fin.add_boite_texte("boite_texte",string.ascii_letters+string.digits+' ',16,(0.2,0.3,0.6,0.1),pourcentage=True)
        self.ecran_fin.add_boutton("save",(0.3,0.42),(0.3,0.1),texte="sauvegarder",color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=self.save,pourcentage=True)
        self.mat = False
        self.is_save = False
        self.game = game

    def afficher(self,surface):
        if not self.parti_en_cour :
            return
        self.echiquier.afficher_case()
        for image in self.preview :
            image.afficher(surface)

        self.echiquier.afficher_piece(surface)
        self.ecran_fin.afficher(surface)

    def save(self):
        name = self.ecran_fin.children["boite_texte"].texte_afficher.texte
        if self.is_save :
            return
        if name in self.game.parti_jouer :
            return
        self.game.parti_jouer[name] = self.echiquier.coup
        with open('save/parti.json','w') as f:
            json.dump(self.game.parti_jouer,f)
        self.is_save = True


    def click(self):
        if not self.parti_en_cour or self.mat:
            return
        x,y = pygame.mouse.get_pos()
        x = int( x // cst.taille_case)
        y = int( y // cst.taille_case)
        if not fct.out_of_board((x,y)):
            return

        if self.echiquier.echiquier[x][y] is not None and self.echiquier.echiquier[x][y].couleur == self.echiquier.couleur_joueur:
            self.changer_piece_selectione(self.echiquier.echiquier[x][y])
        elif not self.piece_selectione is None and (x,y) in self.piece_selectione.coup :
            self.deplacer_piece(self.piece_selectione,(x,y))
            self.changer_piece_selectione(None)
        else:
            self.changer_piece_selectione(None)

    def gerer_mat(self):
        self.mat = True
        self.echiquier.scene_droite.timer_on = False
        self.ecran_fin.add_texte("texte_gagnant",cst.MIDPETITEPOLICE,"le joueur "+self.joueur_gagnant+" a gagner",(0.5,0.05),color="red",iscentre=True,pourcentage=True)
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

class PartiLocal(Parti):
    def __init__(self,game):
        super().__init__(game)
        self.echiquier.preparer_couleur_joue(self.echiquier.couleur_joueur)

    def deplacer_piece(self,piece,destination):
        coup = self.echiquier.creer_coup(piece,destination)
        self.echiquier.jouer_coup(coup)
        self.echiquier.couleur_joueur = autre_couleur(self.echiquier.couleur_joueur)
        self.echiquier.preparer_couleur_joue(self.echiquier.couleur_joueur)
