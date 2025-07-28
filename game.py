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
        self.acceuil.activer_desactiver(True)
        self.check_event()

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
        if event.type == pygame.MOUSEBUTTONUP:
            eventhandler.activer_event(cst.EVENTMOUSEFINCLICK)
        if event.type == pygame.MOUSEMOTION:
            eventhandler.activer_event(cst.EVENTMOUSEMOTION)
        if event.type == cst.PASSESECONDE :
            eventhandler.activer_event(cst.EVENTPASSESECOND)
        if event.type == pygame.MOUSEWHEEL :
            if event.y == 1:
                eventhandler.activer_event(cst.EVENTSCROLLUP)
            else :
                eventhandler.activer_event(cst.EVENTSCROLLDOWN)


    def aller_au_menu_solo(self):
        self.etat = cst.MENUSOLO
        self.solo = True
        self.acceuil.activer_desactiver(False)
        self.menu_solo.activer_desactiver(True)
        self.parametre.icon_boutton.activer_desactiver(True)

    def aller_a_acceuil(self):
        self.etat = cst.ACCEUIL
        self.solo = False
        self.acceuil.activer_desactiver(True)
        self.menu_solo.activer_desactiver(False)
        self.parametre.icon_boutton.activer_desactiver(False)

    def init_partie_solo(self):
        print('ez')
        self.parti = PartiLocal()
        self.etat = cst.PARTI
        self.menu_solo.activer_desactiver(False)

    def fin_parti(self):
        eventhandler.enlever_event(cst.EVENTMOUSECLICK,self.parti.ecran_fin.children['retour_menu'].est_clique)
        self.parti = None
        self.etat = cst.MENUSOLO
        self.menu_solo.activer_desactiver(True)

    def check_event(self):
        eventhandler.ajouter_event(cst.EVENTLANCER1V1,self.init_partie_solo)
        eventhandler.ajouter_event(cst.EVENTRETOURAUMENUSOLO, self.fin_parti)
        eventhandler.ajouter_event(cst.EVENTALLERAUMENUSOLO, self.aller_au_menu_solo)
        eventhandler.ajouter_event(cst.EVENTALLERAACCEUIL, self.aller_a_acceuil)

