import pygame
from utilitaire.eventhandler import eventhandler
import acceuil
import utilitaire.constante as cst
import utilitaire.fonction_utile as fct
from parametre import Parametre
from parti import Parti,PartiLocal

class Game:
    def __init__(self):
        self.etat = cst.ACCEUIL
        self.parti = None
        self.solo = False
        self.menu_solo = acceuil.menu_solo
        self.acceuil = acceuil.accueil
        self.parametre = Parametre()

    def afficher(self,surface):
        if self.etat == cst.ACCEUIL:
            self.acceuil.afficher(surface)
        if self.etat == cst.MENUSOLO :
            self.menu_solo.afficher(surface)
        if self.etat == cst.PARTI:
            self.parti.afficher(surface)
        if self.solo :
            self.parametre.afficher(surface)

    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            eventhandler.activer_event(cst.EVENTMOUSECLICK)
        if event.type == pygame.MOUSEMOTION:
            eventhandler.activer_event(cst.EVENTMOUSEMOTION)
        if event.type == cst.PASSESECONDE :
            eventhandler.activer_event(cst.EVENTPASSESECOND)


    def aller_au_menu_solo(self):
        self.etat = cst.MENUSOLO
        self.solo = True

    def aller_a_acceuil(self):
        self.etat = cst.ACCEUIL
        self.solo = False

    def init_partie_solo(self):
        self.parti = PartiLocal()
        self.etat = cst.PARTI
        self.parametre.en_parti = True

    def fin_parti(self):
        del self.parti
        self.parti = None
        self.parametre.en_parti = False
        self.etat = cst.MENUSOLO

    def check_event(self):
        eventhandler.activer_event(cst.EVENTLANCER1V1,self.init_partie_solo)
        eventhandler.activer_event(cst.EVENTRETOURAUMENUSOLO, self.fin_parti)
        eventhandler.activer_event(cst.EVENTLANCER1V1, self.init_partie_solo)
        eventhandler.activer_event(cst.EVENTLANCER1V1, self.init_partie_solo)
        # if fct.check_event(cst.LANCER1V1) :
        #     self.init_partie_solo()
        # if fct.check_event(cst.RETOURAUMENUSOLO):
        #     self.fin_parti(cst.MENUSOLO)
        #     self.parametre.est_afficher = False
        # if fct.check_event(cst.ALLERAUMENUSOLO):
        #     self.aller_au_menu_solo()
        # if fct.check_event(cst.ALLERAACCEUIL):
        #     self.aller_a_acceuil()

    def boucle(self):
        self.check_event()
        if cst.mouseclick and self.parti is not None:
            self.parti.click()
        elif self.etat == cst.ACCEUIL :
            self.acceuil.boucle(cst.mouseclick,cst.mousemotion)
        elif self.etat == cst.MENUSOLO:
            self.menu_solo.boucle(cst.mouseclick,cst.mousemotion)
        elif self.etat == cst.PARTI :
            self.parti.boucle()
        if self.solo :
            self.parametre.boucle(cst.mouseclick,cst.mousemotion)
        cst.mousemotion = False
        cst.mouseclick = False
