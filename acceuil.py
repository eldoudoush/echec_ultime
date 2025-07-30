import string

import pygame.event
import json
from utilitaire.eventhandler import eventhandler
import utilitaire.constante as cst
from utilitaire.fonction_utile import AffichageBouttonTexteImage, TexteDeroulant, SurfaceMaison, TexteAfficher


class GestionnaireDadresse(TexteDeroulant):
    def __init__(self,parent,pos,largeur,hauteur, colorbg,taille_scroll):
        super().__init__(parent,"gestionnaireDadresse",pos,largeur,hauteur,colorbg=colorbg,taille_scroll=taille_scroll,active=True)

        self.dic_adresse = {}
        self.adresse = None

    def changer_adresse(self, adresse):
        self.adresse = adresse

    def ajouter_adresse(self, name_adresse):
        print(ajouter_serveur.children["nom"].get_texte(),ajouter_serveur.children["ip"].get_texte())
        name , adresse = name_adresse
        self.dic_adresse[adresse] = name
        adresse = Adresse(None,adresse,pygame.Rect(500,500,self.rect.width-self.rect_scrollbar.width*1.5,self.rect.height/5),texte_name=name,active=self.active,color_bg=cst.BLEUFONCE,colorbg_selectione='black')
        self.add_child(adresse,en_bas=True)
        print(self.children)

    def save(self,fichier):
        json.dump(self.dic_adresse,fichier)

    def load(self,fichier):
        self.dic_adresse = json.load(fichier)

class Adresse(SurfaceMaison):
    def __init__(self,parent:GestionnaireDadresse,name,rect:pygame.Rect,active,color_bg,colorbg_selectione,texte_name):
        super().__init__(parent,name,rect,active=active)
        self.est_selectione = False
        self.color_bg = color_bg
        self.colorbg_selectione = colorbg_selectione
        TexteAfficher(self,"texte",cst.PETITEPOLICE,texte_name,(0.1*self.rect.width,0.1*self.rect.height),color='white',active=self.active)

        eventhandler.ajouter_event(cst.EVENTMOUSECLICK, self.selectione)

    def selectione(self):
        if not self.active :
            return
        selec = self.est_selectione
        if self.detect_rect.collidepoint(pygame.mouse.get_pos()):
            print('hahahaha')
            self.est_selectione = True
        else:
            self.est_selectione = False
        if self.est_selectione != selec :
            self.update_surface()
            if self.est_selectione :
                self.parent.changer_adresse(self.name)

    def update_surface_bonus(self):
        rect_bordure = self.rect.copy()
        rect_bordure.inflate_ip(-int(self.rect.width/20),-int(self.rect.width/20))
        if self.est_selectione :
            self.surface.fill(self.colorbg_selectione)
        else:
            self.surface.fill(self.color_bg)


menu_solo = AffichageBouttonTexteImage('menu_solo',cst.screen.get_rect(),cst.COULEURBG)
menu_solo.add_texte("texte_principale",cst.PETITEPOLICE,"le menu pour les sans ami ;(",(0.05,0.1),pourcentage=True)
menu_solo.add_boutton("1v1",(0.15,0.25),(0.25,0.15),texte='  1v1  ',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTLANCER1V1,pourcentage=True)
menu_solo.add_boutton("bot",(0.15,0.45),(0.25,0.15),texte='  bot  ',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTMODEMULTI,pourcentage=True)
menu_solo.add_boutton("retour_acceuil",(0.65, 0.77), (0.301, 0.165), color=cst.COULEURBOUTONACCEUIL,
                                            color_hover=cst.COULEURBOUTONACCEUILHOVER, texte="retour a l'acceuil",
                                            reponse=cst.EVENTALLERAACCEUIL, pourcentage=True)

accueil = AffichageBouttonTexteImage("acceuil",cst.screen.get_rect(),cst.COULEURBG,active=True)
accueil.add_image("pouce_en_air",(0.65,0.65),(0.3,0.3),"image/pouce_en_air.png",pourcentage=True)
accueil.add_texte("texte_principale",cst.PETITEPOLICE,"bienvenue sur l'acceuil des echecs",(0.05,0.1),pourcentage=True)
accueil.add_boutton("solo",(0.15,0.25),(0.25,0.15),texte='jouer en solo',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTALLERAUMENUSOLO,pourcentage=True)
accueil.add_boutton("multi",(0.15,0.45),(0.25,0.15),texte='jouer en multi',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTALLERAUMENUMULTI,pourcentage=True)


menu_multi =AffichageBouttonTexteImage("menu_multi",cst.screen.get_rect(),couleur_bg=cst.COULEURBG)
GestionnaireDadresse(menu_multi,(cst.width * 0.2, cst.height * 0.2),
                                             cst.width * 0.6, cst.height * 0.6, colorbg=cst.COULEURBGFONCE,taille_scroll=cst.width*0.02)
menu_multi.add_boutton("retour_acceuil",(0.2,0.82),(0.15,0.1),texte="retour a l'acceuil",color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTALLERAACCEUIL,pourcentage=True)
menu_multi.add_texte("texte",cst.PETITEPOLICE,"choisisser un serveur :",(0.1,0.05),pourcentage=True)

ajouter_serveur = AffichageBouttonTexteImage("ajouter_serveur",pygame.Rect(0.15*cst.width,0.15*cst.height,0.7*cst.width,0.7*cst.height),(50,50,50),active=True,parent=menu_multi,changer_active_parent=False)
ajouter_serveur.add_texte("texte_nom",cst.PETITEPOLICE,"entrer un nom :",(0.2,0.15),color='white',pourcentage=True)
ajouter_serveur.add_boite_texte("nom",string.ascii_letters,12,(0.2,0.2,0.6,0.15),pourcentage=True)
ajouter_serveur.add_texte("texte_ip",cst.PETITEPOLICE,"entrer l'IP :",(0.2,0.35),color='white',pourcentage=True)
ajouter_serveur.add_boite_texte("ip",string.ascii_letters,12,(0.2,0.4,0.6,0.15),pourcentage=True)
ajouter_serveur.add_boutton("ajouter",(0.3,0.6),(0.4,0.15),texte="ajouter",color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=(menu_multi.children["gestionnaireDadresse"].ajouter_adresse,(ajouter_serveur.children["nom"].get_texte,ajouter_serveur.children["ip"].get_texte)),pourcentage=True)

menu_multi.add_boutton("ajouter_serveur_boutton",(0.4,0.82),(0.15,0.1),texte="ajouter_serveur",color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=[menu_multi.children["ajouter_serveur"].activer_desactiver,menu_multi.children["gestionnaireDadresse"].activer_desactiver],pourcentage=True)

parti_review = AffichageBouttonTexteImage("menu_multi",cst.screen.get_rect(),couleur_bg=cst.COULEURBG)
GestionnaireDadresse(parti_review,(cst.width * 0.2, cst.height * 0.2),
                                             cst.width * 0.6, cst.height * 0.6, colorbg=cst.COULEURBGFONCE,taille_scroll=cst.width*0.02)
parti_review.add_boutton("retour_acceuil",(0.2,0.82),(0.15,0.08),texte="retour a l'acceuil",color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTALLERAACCEUIL,pourcentage=True)
parti_review.add_texte("texte",cst.PETITEPOLICE,"choisisser un serveur :",(0.1,0.05),pourcentage=True)