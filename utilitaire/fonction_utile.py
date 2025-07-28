from time import sleep

import pygame
from pygame import SurfaceType
import utilitaire.constante as cst
from utilitaire.constante import taille_case
from utilitaire.eventhandler import eventhandler

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

def ajouter_tuple(tuple1:tuple[float,float],tuple2:tuple[float,float]):
    return (tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])

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

class SurfaceMaison:
    def __init__(self,parent,name,rect:pygame.Rect,iscentre=False,scale=(None,None),active=False):
        self.rect = rect
        self.surface = SurfaceType(self.rect.size)
        self.surface.fill((10, 10, 10))
        self.surface.set_colorkey((10, 10, 10))
        self.iscentre = iscentre
        self.scale = scale
        self.active = active
        self.parent = parent
        self.children = {}
        self.name = name

        self.init()
    def activer_desactiver(self,mettre=None):
        if mettre is None:
            self.active = not self.active
        else:
            self.active = mettre
        for child in self.children.values() :
            child.activer_desactiver(self.active)
        self.update_surface()

    def afficher(self,surface):
        if self.active :
            surface.blit(self.surface,self.rect)

    def update_surface(self):
        self.update_surface_bonus()
        for surface in self.children.values():
            surface.afficher(self.surface)
        if self.parent is not None:
            self.parent.update_surface()

    def update_surface_bonus(self):
        pass

    def add_child(self,child):
        self.children[child.name] = child
        child.active = self.active
        self.update_surface()

    def init(self):
        if self.parent is None :
            return
        self.parent.add_child(self)

class Image(SurfaceMaison):
    def __init__(self,parent,name,rect:pygame.Rect,image_path,iscentre=False,scale=(None,None)):
        super().__init__(parent,name,rect,iscentre,scale)
        self.image_path = image_path
        self.update_surface()

    def scale(self,sx=None,sy=None):
        self.scale = (sx,sy)
        self.update_surface()

    def afficher(self, surface: SurfaceType):
        if self.iscentre:
            surface.blit(self.surface, soustraire_tuple(self.rect.topleft,self.rect.center))
        else:
            surface.blit(self.surface, self.rect.topleft)

    def changer_pos(self, pos: tuple[float, float]):
        self.rect = pygame.Rect(pos,self.rect.size)
        self.update_surface()

    def changer_img(self, image_path: str):
        self.image_path = image_path
        self.update_surface()

    def update_surface_bonus(self):
        sx, sy = self.scale
        if sx is not None or sy is not None:
            sx = sx if sx is not None else self.rect.width
            sy = sy if sy is not None else self.rect.height
            self.surface = import_image_resize(self.image_path, (sx, sy))
            return
        self.surface = import_image_resize(self.image_path, self.rect.size)

class TexteAfficher(SurfaceMaison):
    def __init__(self,parent,name,taille_font:int,message:str,pos,color='black',font='font/gau_font_cube/GAU_cube_B.TTF',iscentre=False,scale=(None,None),active=False):
        super().__init__(parent, name, rect=pygame.Rect(pos, (0, 0)),iscentre=iscentre,scale=scale,active=active)
        self.texte = message
        self.taille_font = taille_font
        self.color = color
        self.font = font

        self.update_surface()


    def afficher(self,surface:SurfaceType):
        if not self.active:
            return
        if self.iscentre:
            surface.blit(self.surface,soustraire_tuple(self.rect.center,self.rect.size))
            return
        surface.blit(self.surface,self.rect)

    def changer_pos(self,pos:tuple[int,int]):
        self.rect = pygame.Rect(pos,self.rect.size)
        self.update_surface()

    def changer_texte(self,message:str):
        self.texte = message
        self.update_surface()

    def update_surface_bonus(self):
        self.surface = cree_texte(self.taille_font, self.texte, color=self.color, font=self.font)
        sx,sy = self.scale
        if sx is not None or sy is not None :
            sx = sx if sx is not None else self.surface.get_rect().width
            sy = sy if sy is not None else self.surface.get_rect().height
            self.surface = pygame.transform.scale(self.surface,(sx,sy))
        self.rect = pygame.Rect(self.rect.topleft,self.surface.get_rect().size)

    def scale(self,sx=None,sy=None):
        self.scale = (sx,sy)
        self.update_surface()

class TexteDeroulant(SurfaceMaison):
    def __init__(self,parent,name,pos:tuple[float,float],largeur:float,hauteur:float,ecart=10,active=False,colorbg='black'):
        super().__init__(parent,name,pygame.Rect(pos,(largeur,hauteur)),active=active)
        self.ecart = ecart
        self.ind = 0
        self.plus_haute_surface = 0
        self.rect_arriere_scrollbar = pygame.Rect(largeur*11/12,0,largeur/12,hauteur)
        self.scroll_speed = 30
        self.rect_scrollbar = pygame.Rect(largeur*11/12,0,largeur/12,hauteur)
        self.surface_reel = SurfaceType((largeur, 0))
        self.lst_surface = []
        self.drag = False
        self.surface_afficher = SurfaceType((largeur,hauteur))
        self.colorbg= colorbg
        eventhandler.ajouter_event(cst.EVENTSCROLLUP,self.scroll_up)
        eventhandler.ajouter_event(cst.EVENTSCROLLDOWN, self.scroll_down)
        eventhandler.ajouter_event(cst.EVENTMOUSECLICK, self.click)
        eventhandler.ajouter_event(cst.EVENTMOUSEFINCLICK, self.finclick)
        eventhandler.ajouter_event(cst.EVENTMOUSEMOTION, self.motion)
        self.update_surface()

    def motion(self):
        if not self.active:
            return
        if self.drag:
            taille_reel = self.surface_reel.get_height() if self.surface_reel.get_height() > 1 else 1
            self.changer_ind(pygame.mouse.get_rel()[1]*(taille_reel / self.rect.height))

    def finclick(self):
        self.drag = False

    def click(self):
        if not self.active:
            return
        rect = self.rect_scrollbar.move(self.rect.topleft)
        if rect.collidepoint(pygame.mouse.get_pos()):
            self.drag = True

    def update_surface(self,ajout=True):
        self.surface.fill(self.colorbg)
        if ajout :
            taille_reel = 0
            for elem in self.lst_surface :
                taille_reel += elem.rect.height + self.ecart
            self.surface_reel = SurfaceType((self.rect.width, taille_reel))
            self.surface_reel.fill(self.colorbg)
        for elem in self.lst_surface :
            elem.afficher(self.surface_reel)
        self.actualiser_scrollbar()

        self.surface.blit(self.surface_reel,(0,-self.ind))
        pygame.draw.rect(self.surface, (70, 70, 70), self.rect_arriere_scrollbar)
        pygame.draw.rect(self.surface, (150, 150, 150), self.rect_scrollbar)

    def actualiser_scrollbar(self):
        taille_reel = self.surface_reel.get_height() if self.surface_reel.get_height() > 1 else 1
        taille_scrollbar = (self.rect.height / taille_reel) * self.rect.height
        self.rect_scrollbar = pygame.Rect(self.rect_scrollbar.x,self.ind*(self.rect.height / taille_reel),self.rect_scrollbar.width,taille_scrollbar)

    def scroll_up(self):
        if not self.active:
            return
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return
        if not self.drag:
            self.changer_ind(-self.scroll_speed)

    def scroll_down(self):
        if not self.active:
            return
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return
        if not self.drag:
            self.changer_ind(self.scroll_speed)

    def add_child(self,surface,en_haut=False,en_bas=False):
        # if surface.rect.width > self.rect.width - self.rect_scrollbar.width :
        #     surface.scale(sx=self.rect.width -self.rect_scrollbar.width)
        if en_haut:
            self.lst_surface.insert(0,surface)
            ind = self.ecart
            for elem in self.lst_surface:
                height = elem.rect.height
                elem.changer_pos((0, ind))
                ind += self.ecart + height
        elif en_bas:
            self.lst_surface.append(surface)
            ind = self.ecart
            for elem in self.lst_surface:
                height = elem.rect.height
                elem.changer_pos((0,ind))
                ind += self.ecart + height
        else:
            self.lst_surface.append(surface)
        surface.parent = self
        self.children[surface.name] = surface

        self.update_surface()

    def changer_ind(self,value):
        ind = self.ind
        self.ind += value
        if self.ind < 0:
            self.ind = 0
        if self.ind > self.surface_reel.get_height() - self.rect.height :
            self.ind = self.surface_reel.get_height() - self.rect.height
            if self.ind < 0 :
                self.ind = 0
        for elem in self.lst_surface :
            if type(elem) == Boutton :
                elem.detect_rect = elem.rect.move((0, self.ind -ind))
        self.update_surface(ajout=False)


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

class Boutton(SurfaceMaison):
    def __init__(self,parent,name,pos,taille,img=None,texte=None,color=(10,10,10),color_hover=None,reponse=None,class_mere=None,correction=(0,0),active=True,scale=(None,None)):
        super().__init__(parent,name,pygame.rect.Rect(pos,taille),scale=scale)
        self.color_info = color
        self.color_hover = color_hover
        self.color = color
        sx,sy = taille
        img = Image(self,"image",pygame.Rect((0,0),self.rect.size),img) if img is not None else None
        if img is not None :
            self.add_child(img)
        x,y = self.surface.get_rect().center
        texte = TexteAfficher(self,"texte principal",int(sx/len(texte)),texte,(x,y),iscentre=True) if texte is not None else None
        if texte is not None :
            self.add_child(texte)
        self.reponse = reponse
        self.detect_rect = self.rect.move(correction)
        self.init_event()

        self.update_surface()
    def init_event(self):
        eventhandler.ajouter_event(cst.EVENTMOUSECLICK, self.est_clique)
        eventhandler.ajouter_event(cst.EVENTMOUSEMOTION, self.hover)

    def scale(self,sx=None,sy=None):
        self.scale_value = (sx,sy)
        self.update_surface()

    def est_clique(self):
        if not self.active :
            return
        pos = pygame.mouse.get_pos()
        if self.detect_rect.collidepoint(pos):
            if self.reponse is not None :
                eventhandler.activer_event(self.reponse)
    def changer_pos(self, pos: tuple[float, float]):
        self.rect = pygame.Rect(pos,self.rect.size)
        self.update_surface()

    def hover(self):
        if self.color_hover is None:
            return
        if self.detect_rect.collidepoint(pygame.mouse.get_pos()) :
            if self.color != self.color_hover :
                self.color = self.color_hover
                self.update_surface()
        else :
            if self.color != self.color_info:
                self.color = self.color_info
                self.update_surface()

    def update_surface_bonus(self):
        if self.color is not None :
            self.surface.fill(self.color)
        sx, sy = self.scale
        if sx is not None or sy is not None:
            sx = sx if sx is not None else self.surface.get_rect().width
            sy = sy if sy is not None else self.surface.get_rect().height
            self.surface = pygame.transform.scale(self.surface, (sx, sy))

class AffichageBouttonTexteImage(SurfaceMaison):
    def __init__(self,name,rect:pygame.Rect,couleur_bg=(10,10,10),active=False,parent=None):
        super().__init__(parent,name,rect)
        self.couleur_bg = couleur_bg
        self.surface.set_colorkey((10,10,10))

    def add_boutton(self,name:str,pos:tuple[float,float],taille:tuple[float,float],img=None,texte=None,color=None,color_hover=None,reponse=-1,pourcentage=False):
        if pourcentage :
            x, y = pos
            sx, sy = taille
            x *= self.rect.width
            y *= self.rect.height
            sx *= self.rect.width
            sy *= self.rect.height
            pos = (x,y)
            taille = (sx,sy)
        boutton = Boutton(self,name,pos,taille,img=img,texte=texte,color=color,color_hover=color_hover,reponse=reponse,class_mere=self,correction=self.rect.topleft,active=self.active)
        self.add_child(boutton)

    def add_texte(self,name,taille_font:int,message:str,pos:tuple[float,float],color='black',font='font/gau_font_cube/GAU_cube_B.TTF',iscentre=False,pourcentage=False):
        x,y = pos
        if pourcentage :
            x *= self.rect.width
            y *= self.rect.height
        texte = TexteAfficher(self,name,taille_font,message,(x,y),color=color,font=font,iscentre=iscentre)
        self.add_child(texte)


    def add_image(self,name,pos,taille,image_path,iscentre=False,pourcentage=False):
        if pourcentage :
            x, y = pos
            sx, sy = taille
            x *= self.rect.width
            y *= self.rect.height
            sx *= self.rect.width
            sy *= self.rect.height
            pos = (x,y)
            taille = (sx,sy)
        image = Image(self,name,pygame.Rect(pos,taille),image_path,iscentre=iscentre)
        self.add_child(image)