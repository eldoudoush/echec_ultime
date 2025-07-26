import pygame.event

import utilitaire.constante as cst
from utilitaire.fonction_utile import AffichageBouttonTexteImage

menu_solo = AffichageBouttonTexteImage(cst.screen.get_rect(),cst.COULEURBG)
menu_solo.add_texte(cst.PETITEPOLICE,"le menu pour les sans ami ;(",(0.05,0.1),pourcentage=True)
menu_solo.add_boutton((0.15,0.25),(0.25,0.15),texte='  1v1  ',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.LANCER1V1,pourcentage=True)
menu_solo.add_boutton((0.15,0.45),(0.25,0.15),texte='  bot  ',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.MODEMULTI,pourcentage=True)
menu_solo.add_boutton((0.65, 0.77), (0.301, 0.165), color=cst.COULEURBOUTONACCEUIL,
                                            color_hover=cst.COULEURBOUTONACCEUILHOVER, texte="retour a l'acceuil",
                                            reponse=cst.ALLERAACCEUIL, pourcentage=True)

accueil = AffichageBouttonTexteImage(cst.screen.get_rect(),cst.COULEURBG)
accueil.add_image((0.65,0.65),(0.3,0.3),"image/pouce_en_air.png",pourcentage=True)
accueil.add_texte(cst.PETITEPOLICE,"bienvenue sur l'acceuil des echecs",(0.05,0.1),pourcentage=True)
accueil.add_boutton((0.15,0.25),(0.25,0.15),texte='jouer en solo',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.ALLERAUMENUSOLO,pourcentage=True)
accueil.add_boutton((0.15,0.45),(0.25,0.15),texte='jouer en multi',color=cst.COULEURBOUTONACCEUIL,color_hover=cst.COULEURBOUTONACCEUILHOVER,reponse=cst.ALLERAUMENUMULTI,pourcentage=True)