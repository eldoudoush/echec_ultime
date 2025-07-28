import pygame
import string
import utilitaire.constante as cst
import utilitaire.fonction_utile as fct
from utilitaire.eventhandler import eventhandler

class SceneDroite:

    def __init__(self,echiquier):
        self.timer_on = True
        self.timer = {"blanc":cst.timer_blanc,"noir":cst.timer_noir}
        self.timer_minute = {"blanc":"","noir":""}
        self.coup_joue = {"blanc":[],"noir":[]}
        # self.piece_blanc_manger = AffichagePionManger('blanc')
        # self.piece_noir_manger = AffichagePionManger('noir')
        self.texte_timer = {"blanc":fct.TexteAfficher(None,"timer_blanc",cst.PETITEPOLICE,"",(cst.height+(0.1*(cst.width-cst.height)),cst.height/8),color='white',active=True),
                            "noir":fct.TexteAfficher(None,"timer_noir",cst.PETITEPOLICE,"",(cst.height+(0.6*(cst.width-cst.height)),cst.height/8),active=True)}

        self.echiquier = echiquier
        self.afficher_coup = {"blanc":fct.TexteDeroulant(None,'noir',(0.05*(cst.width-cst.height)+cst.height,cst.height/4),0.4*(cst.width-cst.height),cst.height*0.35,active=True),
                              "noir":fct.TexteDeroulant(None,'blanc',(0.55*(cst.width-cst.height)+cst.height,cst.height/4),0.4*(cst.width-cst.height),cst.height*0.35,active=True)}
        eventhandler.ajouter_event(cst.EVENTPASSESECOND,self.temp_timer_reduction)

        self.init_affichage()

    def temp_timer_reduction(self):
        couleur = self.echiquier.couleur_joueur
        if self.timer_on :
            self.timer[couleur] -=1
            self.update_text(couleur)
            self.update_affichage(couleur)
            if self.timer[couleur] == 0 :
                self.timer_on = False
                self.echiquier.parti.parti_en_cour = False
                self.echiquier.parti.joueur_gagnant = fct.autre_couleur(couleur)

    def update_text(self,couleur):
        self.timer_minute[couleur] = str(self.timer[couleur] // 60) + ':' + (
            '0' if self.timer[couleur] % 60 < 10 else '') + str(self.timer[couleur] % 60)

    def update_affichage(self,couleur):
        self.texte_timer[couleur].changer_texte(self.timer_minute[couleur])

    def afficher(self,surface):
        for texte in self.texte_timer.values():
            texte.afficher(surface)
        for elem in self.afficher_coup.values():
            elem.afficher(surface)

    def ajouter_coup(self,coup):
        self.coup_joue[coup[5]].append(coup)
        if coup[6] is None :
            texte = fct.TexteAfficher(None,"",cst.TRESPETITEPOLICE, self.creer_texte(coup), (0, 0), color='white',active=True)
        else :
            texte = fct.TexteAfficher(None,"",cst.TRESPETITEPOLICE, coup[6], (0, 0), color='white')
        self.afficher_coup[coup[5]].add_child(texte,en_bas=True)

    def creer_texte(self,coup):
        alphabet = string.ascii_lowercase
        dic_Piece_anglais = {'p' : 'P','d' : 'Q','t' : 'R','r' : 'K','f' : 'B','c': 'C'}
        case = alphabet[coup[0][0]] + str(coup[0][1]+1)
        case_arriver = alphabet[coup[2][0]] + str(coup[2][1]+1)
        texte = dic_Piece_anglais[coup[1][0]] + case + ' ' + case_arriver
        print(coup[3])
        if coup[3] is not None:
            texte += 'x' + dic_Piece_anglais[coup[3][0]]
        return texte

    def init_affichage(self):
        self.update_text("blanc")
        self.update_text("noir")
        self.update_affichage("blanc")
        self.update_affichage("noir")



class AffichagePionManger:
    def __init__(self,couleur):
        self.couleur = couleur
        self.screen = screen
        self.screen_height = screen.get_height()
        self.origine = (self.screen_height, 0)
        self.width = self.screen.get_width() - self.screen_height

        self.liste_piece_manger =[]
        self.dic_piece = {'pion':0,'cheval':0,'dame':0,'roi':0,'fou':0,'tour':0}
        self.dic_emplacement_piece = {'pion':self.pos(0,0),'cheval':self.pos(1,0),'dame':self.pos(2,0),'roi':self.pos(2,1),'fou':self.pos(0,1),'tour':self.pos(1,1)}
        self.dic_Piece_anglais = {'p' : 'P','d' : 'Q','t' : 'R','r' : 'K','f' : 'B','c': 'C'}
        self.dic_texte_piece = {'pion':None,'cheval':None,'dame':None,'roi':None,'fou':None,'tour':None}
        self.font_size =  self.width // 30
        self.font = pygame.font.Font('pieces_echecs/gau_font_cube/GAU_cube_B.TTF',self.font_size)

    def creer_texte(self,piece):
        self.liste_piece_manger.append(piece)
        piece_nom = piece.piece
        self.dic_piece[piece_nom] += 1
        self.dic_texte_piece[piece_nom] = (self.font.render( str(self.dic_piece[piece_nom])+'x '+self.dic_Piece_anglais[piece_nom[0]], True, (255, 255, 255)), (self.dic_emplacement_piece[piece_nom]))

    def update(self):
        for elem in self.dic_texte_piece.values():
            if not elem is None :
                x,y = elem
                self.screen.blit(x,y)

    def pos(self,x,y):
        if self.couleur == 'blanc':
            x_return = self.screen_height + ((x / 8) * self.width) + 1 * self.width / 40
            y_return = (y+6) * self.screen_height / 8
        else:
            x_return = self.screen_height + (((x+5) / 8) * self.width)
            y_return =  (y+6) * self.screen_height / 8
        return (x_return,y_return)

    def clear(self):
        self.liste_piece_manger = []
        # self.dic_piece = {'pion': 0, 'cheval': 0, 'dame': 0, 'roi': 0, 'fou': 0, 'tour': 0}
        # self.dic_emplacement_piece = {'pion': self.pos(0, 0), 'cheval': self.pos(1, 0), 'dame': self.pos(2, 0),
        #                               'roi': self.pos(0, 1), 'fou': self.pos(1, 1), 'tour': self.pos(2, 1)}
        # self.dic_texte_piece = {'pion': None, 'cheval': None, 'dame': None, 'roi': None, 'fou': None, 'tour': None}
        self.__init__(self.screen ,self.couleur)