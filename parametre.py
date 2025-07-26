import utilitaire.constante as cst
import utilitaire.fonction_utile as fct
import pygame

from utilitaire.fonction_utile import AffichageBouttonTexteImage

class Parametre:

    def __init__(self,):
        self.interface = AffichageBouttonTexteImage(pygame.Rect(cst.width//8,cst.height//8,cst.width*6//8,cst.height*6//8))
        self.icon_boutton = fct.Boutton((14.5*cst.width//16,cst.height/100),(cst.width//12,cst.width//12,),'image/image_parametre/engrenage_parametre.png',reponse=cst.ICONREGLAGE)
        self.est_afficher = False
        self.interface.add_image((0,0),(1,1),'image/image_parametre/parametre_bg.png',pourcentage=True)
        self.interface_en_parti = AffichageBouttonTexteImage(pygame.Rect(cst.width//8,cst.height//8,cst.width*6//8,cst.height*6//8))
        self.interface_en_parti.add_boutton((0.65,0.77),(0.301,0.165),color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,texte="retour au menu",reponse=cst.RETOURAUMENUSOLO,pourcentage=True)
        self.en_parti = False

    def afficher(self,surface):
        self.icon_boutton.afficher(surface)
        if self.est_afficher :
            self.interface.afficher(surface)
            if self.en_parti :
                self.interface_en_parti.afficher(surface)


    def boucle(self,click,motion):
        if click:
            self.icon_boutton.est_clique()
        if fct.check_event(cst.ICONREGLAGE):
            self.est_afficher = not self.est_afficher
        if self.est_afficher :
            self.interface.boucle(click, motion)
            if self.en_parti :
                self.interface_en_parti.boucle(click,motion)