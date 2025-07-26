import pygame

pygame.font.init()
pygame.sysfont.initsysfonts()

#screen
size = (1500,1000)

screen = pygame.display.set_mode(size)

icon = pygame.image.load('image/lenimax.png')

pygame.display.set_caption('surprise')

pygame.display.set_icon(icon)


height = screen.get_height()
width = screen.get_width()

font_path = 'font/gau_font_cube/GAU_cube_B.TTF'
#dic

#event
PASSESECONDE = pygame.USEREVENT + 1
mousemotion = False
mouseclick = False

EVENTLANCER1V1 = 0
EVENTMODEMULTI = 1
EVENTICONREGLAGE = 2
EVENTRETOURAUMENUSOLO = 3
EVENTALLERAUMENUSOLO = 4
EVENTALLERAUMENUMULTI = 5
EVENTALLERAACCEUIL = 6
EVENTPASSESECOND = 7
EVENT250MS = 8 # pas utiliser
EVENTMOUSECLICK = 9
EVENTMOUSEMOTION = 10

#plateau
plateau_classique = 'RCBQKBCR/PPPPPPPP/8/8/8/8/pppppppp/rcbqkbcr'

#timer
timer_blanc = 30*60
timer_noir = 30*60

#taille chose
PETITEPOLICE = int(width / 32)
MOYENNEPOLICE = int(width / 20)
GRANDEPOLICE = int(width/14)
TRESGRANDEPOLICE = int(width / 8)
taille_case = height / 8

#couleur
COULEURBG = (0,25,200)
COULEURBOUTONACCEUIL = (50,200,0)
COULEURBOUTONACCEUILHOVER = (50,150,0)
couleur_case_blanche = (255,255,255)
couleur_case_fonce = (58,34,10)

#ETAT DU JEU
ACCEUIL = 0
MENUSOLO = 2
MENUENLIGNE = 9
PARTI = 10

#const scene_droite
sd_font =  pygame.font.Font('font/gau_font_cube/GAU_cube_B.TTF', GRANDEPOLICE)
sd_origine = (height,0)
sd_pos_blanc = (height + ((1 / 8) * width), height / 8)
sd_pos_noir = (height + ((5 / 8) * width), height / 8)
