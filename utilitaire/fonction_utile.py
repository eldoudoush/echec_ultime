import pygame
from pygame import SurfaceType

pygame.font.init()
pygame.sysfont.initsysfonts()

def import_image_resize(image_input:str,taille:tuple[float,float] ):
    image = pygame.image.load(image_input)
    image = pygame.transform.scale(image , taille)
    return image

def cree_texte(taille_font:int,message:str,color='black',font='font/gau_font_cube/GAU_cube_B.TTF'):
    font = pygame.font.Font(font, taille_font)
    texte = font.render(message, True, color)
    return texte

def clicker(rect:pygame.rect.Rect,pos:tuple) -> bool:
    x,y = pos
    return rect.x <= x <= rect.width + rect.x and rect.y <= y <= rect.height + rect.y

def soustraire_tuple(tuple1:tuple[float,float],tuple2:tuple[float,float]):
    return (tuple1[0]-tuple2[0],tuple1[1]-tuple2[1])

def out_of_board(coordone):
    """
    :param coordone: tuple modelisant un coordone
    :return: True si a est dans l'echiquier False sinon
    """
    x, y = coordone
    return 0 <= x <= 7 and 0 <= y <= 7

def autre_couleur(couleur):
    if couleur == 'blanc':
        return "noir"
    return "blanc"

set_event = set()

def check_event(event):
    if event in set_event :
        set_event.remove(event)
        return True
    return False

class Image:
    def __init__(self,rect:pygame.Rect,image_path,iscentre=False):
        self.rect = rect
        self.image_path = image_path
        self.iscentre = iscentre
        self.image_surface = None

        self.update_affichage()

    def afficher(self, surface: SurfaceType):
        if self.iscentre:
            surface.blit(self.image_surface, soustraire_tuple(self.rect.topleft,self.rect.center))
        else:
            surface.blit(self.image_surface, self.rect.topleft)

    def changer_pos(self, pos: tuple[float, float]):
        self.rect = pygame.Rect(pos,self.rect.size)
        self.update_affichage()

    def changer_img(self, image_path: str):
        self.image_path = image_path
        self.update_affichage()

    def update_affichage(self):
        self.image_surface = import_image_resize(self.image_path, self.rect.size)

class TexteAfficher:
    def __init__(self,taille_font:int,message:str,pos,color='black',font='font/gau_font_cube/GAU_cube_B.TTF',iscentre=False,class_mere=None):
        self.class_mere = class_mere
        self.texte = message
        self.taille_font = taille_font
        self.pos = pos
        self.color = color
        self.font = font
        self.iscentre = iscentre
        self.texte_surface = None
        self.render_pos = pos
        self.update_affichage()

    def afficher(self,surface:SurfaceType):
        surface.blit(self.texte_surface,self.render_pos)

    def chager_pos(self,pos:tuple[int,int]):
        self.pos = pos
        self.update_affichage()

    def changer_texte(self,message:str):
        self.texte = message
        self.update_affichage()

    def update_affichage(self):
        x, y = self.pos
        self.texte_surface = cree_texte(self.taille_font, self.texte, color=self.color, font=self.font)
        if self.iscentre:
            i,j = self.texte_surface.get_rect().center
            self.render_pos = (x-i,y-j)
        if self.class_mere is not None:
            self.class_mere.actualiser_affichage()

class TexteDeroulant:
    def __init__(self,pos:tuple[float,float],largeur:float,hauteur:float):
        self.pos = pos
        self.hauteur = hauteur
        self.taille = (largeur,hauteur)
        self.surface = pygame.rect.Rect(pos,self.taille)
        self.lst_surface = []
    def ajouter_surface(self,surface):
        self.lst_surface.append(surface)


class BoiteTexte:
    def __init__(self,screen,restriction:str,taille_limite,rect:list[int],texte_originel:str=''):
        self.texte = texte_originel
        self.restriction = restriction
        self.taille_limite = taille_limite
        self.rect = rect
        x,y,sx,sy = rect
        self.font_size = int(sy*2/3)
        self.est_clicker = False
        self.texte_afficher,self.pos_texte = cree_texte(self.font_size,self.texte,int(x+sx/12),int(y+sy/6))
        self.screen = screen

    def update(self):
        pygame.draw.rect(self.screen,'white',self.rect)
        pygame.draw.rect(self.screen, 'black', self.rect, 3)
        self.screen.blit(self.texte_afficher,self.pos_texte)

    def changer_texte(self,texte):
        self.texte = texte
        self.texte_afficher, self.pos_texte = cree_texte(self.font_size, self.texte, self.pos_texte[0], self.pos_texte[1])

    def ajouter_texte(self,entrer:str):
        if not entrer in self.restriction:
            return
        if len(self.texte) >= self.taille_limite:
            return
        self.texte += entrer
        self.texte_afficher, self.pos_texte = cree_texte(self.font_size, self.texte, self.pos_texte[0], self.pos_texte[1])

    def suprimer_texte(self):
        if self.texte == '':
            return
        self.texte = self.texte[:len(self.texte) - 1]
        self.texte_afficher, self.pos_texte = cree_texte(self.font_size, self.texte, self.pos_texte[0],
                                                         self.pos_texte[1])

class GestionnaireDeBoiteTexte:
    def __init__(self):
        self.liste_boitetexte = []

    def append(self,boitetexte:BoiteTexte):
        self.liste_boitetexte.append(boitetexte)

    def uptdate(self):
        for elem in self.liste_boitetexte:
            elem.update()

    def activer_boitetexte(self,pos_curseur):
        for elem in self.liste_boitetexte:
            elem.est_clicker = False
            if clicker(elem.rect,pos_curseur):
                elem.est_clicker = True

    def ajouter_boitetexte(self,event):
        for elem in self.liste_boitetexte:
            if elem.est_clicker:
                if event.key == pygame.K_BACKSPACE:
                    elem.suprimer_texte()
                else:
                    elem.ajouter_texte(event.unicode)

class Boutton:
    def __init__(self,pos,taille,img=None,texte=None,color=(10,10,10),color_hover=None,reponse=None,class_mere=None,correction=(0,0)):
        self.surface = SurfaceType(taille)
        self.surface.set_colorkey((10,10,10))
        self.rect = pygame.rect.Rect(pos,taille)
        self.color_info = color
        self.color_hover = color_hover
        self.color = color
        x,y = pos
        sx,sy = taille
        self.img = Image(pygame.Rect((0,0),self.rect.size),img) if img is not None else None
        x,y = self.surface.get_rect().center
        self.texte = TexteAfficher(int(sx/len(texte)),texte,(x,y),iscentre=True) if texte is not None else None
        self.reponse = reponse
        self.class_mere = class_mere
        self.detect_rect = self.rect.move(correction)

        self.actualiser_affichage()

    def est_clique(self):
        pos = pygame.mouse.get_pos()
        if self.detect_rect.collidepoint(pos):
            if self.reponse is not None :
                set_event.add(self.reponse)
    def hover(self):
        if self.color_hover is None:
            return
        if self.detect_rect.collidepoint(pygame.mouse.get_pos()) :
            if self.color != self.color_hover :
                self.color = self.color_hover
                self.actualiser_affichage()
        else :
            if self.color != self.color_info:
                self.color = self.color_info
                self.actualiser_affichage()

    def actualiser_affichage(self):
        if self.color is not None :
            self.surface.fill(self.color)
        if self.img is not None :
            self.img.afficher(self.surface)
        if self.texte is not None:
            self.texte.afficher(self.surface)
        if self.class_mere is not None :
            self.class_mere.actualiser_affichage()

    def afficher(self,surface:SurfaceType):
        self.hover()
        surface.blit(self.surface, self.rect)

class AffichageBouttonTexteImage:
    def __init__(self,rect:pygame.Rect,couleur_bg=(10,10,10)):
        self.rect = rect
        self.couleur_bg = couleur_bg
        self.surface = pygame.Surface(self.rect.size)
        self.surface.set_colorkey((10,10,10))
        self.lst_texte = []
        self.lst_image = []
        self.lst_boutton = []

    def actualiser_affichage(self):
        self.surface.fill(self.couleur_bg)
        for image in self.lst_image :
            image.afficher(self.surface)
        for texte in self.lst_texte:
            texte.afficher(self.surface)
        for boutton in self.lst_boutton :
            boutton.afficher(self.surface)

    def afficher(self,surface:SurfaceType):
        surface.blit(self.surface,self.rect)

    def add_boutton(self,pos:tuple[float,float],taille:tuple[float,float],img=None,texte=None,color=None,color_hover=None,reponse=-1,pourcentage=False):
        if pourcentage :
            x, y = pos
            sx, sy = taille
            x *= self.rect.width
            y *= self.rect.height
            sx *= self.rect.width
            sy *= self.rect.height
            pos = (x,y)
            taille = (sx,sy)
        self.lst_boutton.append(Boutton(pos,taille,img=img,texte=texte,color=color,color_hover=color_hover,reponse=reponse,class_mere=self,correction=self.rect.topleft))
        self.actualiser_affichage()

    def add_texte(self,taille_font:int,message:str,pos:tuple[float,float],color='black',font='font/gau_font_cube/GAU_cube_B.TTF',iscentre=False,pourcentage=False):
        x,y = pos
        if pourcentage :
            x *= self.rect.width
            y *= self.rect.height
        self.lst_texte.append(TexteAfficher(taille_font,message,(x,y),color=color,font=font,iscentre=iscentre,class_mere=self))
        self.actualiser_affichage()

    def gerer_inpout_boutton(self,click,motion):
        if motion :
            for boutton in self.lst_boutton:
                boutton.hover()
        if click :
            for boutton in self.lst_boutton:
                boutton.est_clique()

    def add_image(self,pos,taille,image_path,iscentre=False,pourcentage=False):
        if pourcentage :
            x, y = pos
            sx, sy = taille
            x *= self.rect.width
            y *= self.rect.height
            sx *= self.rect.width
            sy *= self.rect.height
            pos = (x,y)
            taille = (sx,sy)
        self.lst_image.append(Image(pygame.Rect(pos,taille),image_path,iscentre=iscentre))
        self.actualiser_affichage()

    def boucle(self,click,motion):
        self.gerer_inpout_boutton(click,motion)