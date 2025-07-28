import utilitaire.constante as cst
import utilitaire.fonction_utile as fct
from utilitaire.eventhandler import eventhandler
import pygame

from utilitaire.fonction_utile import AffichageBouttonTexteImage

class Parametre:

    def __init__(self,):
        self.interface = AffichageBouttonTexteImage("interface",pygame.Rect(cst.width//8,cst.height//8,cst.width*6//8,cst.height*6//8))
        self.icon_boutton = fct.Boutton(None,"icon_boutton",(14.5*cst.width//16,cst.height/100),(cst.width//12,cst.width//12,),'image/image_parametre/engrenage_parametre.png',reponse=cst.EVENTICONREGLAGE)
        self.est_afficher = False
        self.en_parti = False
        self.interface.add_image("bg",(0,0),(1,1),'image/image_parametre/parametre_bg.png',pourcentage=True)
        self.interface_en_parti = AffichageBouttonTexteImage("en_parti",pygame.Rect(cst.width//8,cst.height//8,cst.width*6//8,cst.height*6//8))
        self.interface_en_parti.add_boutton("retour au menu",(0.65,0.77),(0.301,0.165),color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,texte="retour au menu",reponse=cst.EVENTRETOURAUMENUSOLO,pourcentage=True)
        eventhandler.ajouter_event(cst.EVENTICONREGLAGE,self.switch_afficher)
        eventhandler.ajouter_event(cst.EVENTLANCER1V1,self.entrer_parti)
        eventhandler.ajouter_event(cst.EVENTRETOURAUMENUSOLO, self.sortir_parti)

    def afficher(self,surface):
        self.icon_boutton.afficher(surface)
        self.interface.afficher(surface)
        self.interface_en_parti.afficher(surface)

    def fermer_param(self):
        self.est_afficher = False
        self.interface.activer_desactiver(False)
        self.interface_en_parti.activer_desactiver(False)

    def entrer_parti(self):
        self.en_parti = True

    def sortir_parti(self):
        self.en_parti = False
        self.est_afficher = False
        self.interface_en_parti.activer_desactiver(False)
        self.interface.activer_desactiver(False)

    def afficher_param(self):
        self.est_afficher = True
        self.interface.activer_desactiver(True)
        if self.en_parti :
            self.interface_en_parti.activer_desactiver(True)

    def switch_afficher(self):
        if self.est_afficher :
            self.fermer_param()
        else:
            self.afficher_param()