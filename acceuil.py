import pygame.event

import utilitaire.constante as cst
from utilitaire.fonction_utile import AffichageBouttonTexteImage

menu_solo = AffichageBouttonTexteImage('menu_solo',cst.screen.get_rect(),cst.COULEURBG)
menu_solo.add_texte("texte_principale",cst.PETITEPOLICE,"le menu pour les sans ami ;(",(0.05,0.1),pourcentage=True)
menu_solo.add_boutton("1v1",(0.15,0.25),(0.25,0.15),texte='  1v1  ',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTLANCER1V1,pourcentage=True)
menu_solo.add_boutton("bot",(0.15,0.45),(0.25,0.15),texte='  bot  ',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTMODEMULTI,pourcentage=True)
menu_solo.add_boutton("retour_acceuil",(0.65, 0.77), (0.301, 0.165), color=cst.COULEURBOUTONACCEUIL,
                                            color_hover=cst.COULEURBOUTONACCEUILHOVER, texte="retour a l'acceuil",
                                            reponse=cst.EVENTALLERAACCEUIL, pourcentage=True)

menu_multi = AffichageBouttonTexteImage('menu_multi',cst.screen.get_rect(),cst.COULEURBG)

accueil = AffichageBouttonTexteImage("acceuil",cst.screen.get_rect(),cst.COULEURBG,active=True)
accueil.add_image("pouce_en_air",(0.65,0.65),(0.3,0.3),"image/pouce_en_air.png",pourcentage=True)
accueil.add_texte("texte_principale",cst.PETITEPOLICE,"bienvenue sur l'acceuil des echecs",(0.05,0.1),pourcentage=True)
accueil.add_boutton("solo",(0.15,0.25),(0.25,0.15),texte='jouer en solo',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTALLERAUMENUSOLO,pourcentage=True)
accueil.add_boutton("multi",(0.15,0.45),(0.25,0.15),texte='jouer en multi',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.EVENTALLERAUMENUMULTI,pourcentage=True)