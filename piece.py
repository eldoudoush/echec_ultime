import pygame

from utilitaire import fonction_utile as fct
from utilitaire import constante as cst


class Piece:
    def __init__(self, x, y, couleur, piece, image, val,echiquier):
        self.premier_coup = True
        self.couleur = couleur
        self.piece = piece
        self.peut_jouer = True
        self.coup = []
        self.val = val
        self.coordone = (x, y)
        self.image_path = image
        tc = cst.taille_case
        x, y = self.coordone
        self.image =  fct.Image(None,piece,pygame.Rect( tc * x, tc * y, tc, tc),self.image_path)
        self.rect = None
        self.echiquier = echiquier
        self.mort = False
        self.visible = True

    def changer_pos(self,pos):
        """
        met a jour la position de la piece en fonction de la case où elle est
        """
        self.coordone = pos
        x,y = pos
        self.image.changer_pos((cst.taille_case * x,cst.taille_case * y))

    def afficher(self,surface):
        if self.mort :
            return
        self.image.afficher(surface)

    def calcul_coup(self,calcul=True):
        pass

    def __str__(self):
        return self.piece


class Pion(Piece):
    def __init__(self, x, y, couleur,echiquier):
        if couleur == 'blanc':
            image = 'image/pieces_echecs/pion_blanc.png'
        else:
            image = 'image/pieces_echecs/pion_noir.png'
        super().__init__(x, y, couleur, 'pion', image, 10,echiquier)

    def calcul_coup(self, calcul=True, detect_enpassent=True):
        self.coup.clear()
        if not self.peut_jouer :
            return
        x, y = self.coordone
        if self.couleur == 'blanc':
            if self.premier_coup:
                for i in range(1, 3):
                    if not self.echiquier.echiquier[x][y - i] is None:
                        break
                    else:
                        ajoute_coup_pas_echec(self, (x, y - i),self.echiquier, calcul=calcul)
            else:
                if self.echiquier.echiquier[x][y - 1] is None:
                    ajoute_coup_pas_echec(self, (x, y - 1),self.echiquier, calcul=calcul)

            for i in range(x-1,x+2,2):
                # detect prise
                if fct.out_of_board((i, y - 1)) and not self.echiquier.echiquier[i][y - 1] is None and \
                        self.echiquier.echiquier[i][y - 1].couleur != self.couleur:
                    ajoute_coup_pas_echec(self, (i, y - 1),self.echiquier, calcul=calcul)

                # detect enpassant
                if fct.out_of_board((i, y)) and not self.echiquier.echiquier[i][y] is None and self.echiquier.echiquier[i][
                    y].couleur != self.couleur:
                    if self.echiquier.echiquier[i][y] in self.echiquier.show_ep() and detect_enpassent:
                        ajoute_coup_pas_echec(self, (i, y - 1),self.echiquier, calcul=calcul)

        else:
            if self.premier_coup:
                for i in range(1, 3):
                    if not self.echiquier.echiquier[x][y + i] is None:
                        break
                    else:
                        ajoute_coup_pas_echec(self, (x, y + i),self.echiquier, calcul=calcul)
            else:
                if fct.out_of_board((x,y + 1)) and self.echiquier.echiquier[x][y + 1] is None:
                    ajoute_coup_pas_echec(self, (x, y + 1),self.echiquier, calcul=calcul)
            # detect prise
            for i in range(x-1,x+2,2):
                if fct.out_of_board((i, y + 1)) and not self.echiquier.echiquier[i][y + 1] is None and \
                        self.echiquier.echiquier[i][y + 1].couleur != self.couleur:
                    ajoute_coup_pas_echec(self, (i, y + 1),self.echiquier, calcul=calcul)

                # detect enpassant
                if fct.out_of_board((i, y)) and not self.echiquier.echiquier[i][y] is None and self.echiquier.echiquier[i][
                    y].couleur != self.couleur:
                    if self.echiquier.echiquier[i][y] in self.echiquier.show_ep() and detect_enpassent:
                        ajoute_coup_pas_echec(self, (i, y + 1),self.echiquier, calcul=calcul)


class Cheval(Piece):
    def __init__(self, x, y, couleur,echiquier):
        if couleur == 'blanc':
            image = 'image/pieces_echecs/cheval_blanc.png'
        else:
            image = 'image/pieces_echecs/cheval_noir.png'
        super().__init__(x, y, couleur, 'cheval', image, 30,echiquier)

    def calcul_coup(self,calcul=True):
        self.coup.clear()
        if not self.peut_jouer :
            return
        x,y = self.coordone
        for elem in [(x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2), (x + 2, y - 1), (x + 2, y + 1),
                     (x - 2, y - 1), (x - 2, y + 1)]:
            a, b = elem
            if fct.out_of_board(elem) and self.echiquier.echiquier[a][b] is None:
                ajoute_coup_pas_echec(self, (a, b), self.echiquier, roi=False, calcul=calcul)
            elif fct.out_of_board(elem) and self.echiquier.echiquier[a][b].couleur != self.couleur:
                ajoute_coup_pas_echec(self, (a, b), self.echiquier, roi=False, calcul=calcul)


class Fou(Piece):
    def __init__(self, x, y, couleur,echiquier):
        if couleur == 'blanc':
            image = 'image/pieces_echecs/fou_blanc.png'
        else:
            image = 'image/pieces_echecs/fou_noir.png'
        super().__init__(x, y, couleur, 'fou', image, 30,echiquier)
    def calcul_coup(self,calcul=True):
        self.coup.clear()
        if not self.peut_jouer :
            return
        for vecteur in [(1,1),(-1,1),(-1,-1),(1,-1)] :
            calcul_coup_vecteur(self,self.echiquier,vecteur,calcul=calcul)

class Tour(Piece):
    def __init__(self, x, y, couleur,echiquier):
        if couleur == 'blanc':
            image = 'image/pieces_echecs/tour_blanc.png'
        else:
            image = 'image/pieces_echecs/tour_noir.png'
        super().__init__(x, y, couleur, 'tour', image, 50,echiquier)
    def calcul_coup(self,calcul=True):
        self.coup.clear()
        if not self.peut_jouer :
            return
        for vecteur in [(1,0),(0,1),(-1,0),(0,-1),] :
            calcul_coup_vecteur(self,self.echiquier,vecteur,calcul=calcul)

class Reine(Piece):
    def __init__(self, x, y, couleur,echiquier):
        if couleur == 'blanc':
            image = 'image/pieces_echecs/reine_blanc.png'
        else:
            image = 'image/pieces_echecs/reine_noir.png'
        super().__init__(x, y, couleur, 'dame', image, 90,echiquier)
    def calcul_coup(self,calcul=True):
        self.coup.clear()
        if not self.peut_jouer :
            return
        for vecteur in [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)] :
            calcul_coup_vecteur(self,self.echiquier,vecteur,calcul=calcul)

class Roi(Piece):
    def __init__(self, x, y, couleur,echiquier):
        if couleur == 'blanc':
            image = 'image/pieces_echecs/roi_blanc.png'
        else:
            image = 'image/pieces_echecs/roi_noir.png'
        super().__init__(x, y, couleur, 'roi', image, 900,echiquier)
        self.img_roi_rouge = 'image/pieces_echecs/roi_rouge.png'
        self.roi_en_echec = False

    def roi_echec(self):
        self.roi_en_echec = True
        self.image.changer_img(self.img_roi_rouge)

    def enlever_echec(self):
        if self.roi_en_echec:
            self.image.changer_img(self.image_path)


    def calcul_coup(self,calcul=True):
        self.coup.clear()
        if not self.peut_jouer :
            return
        x,y = self.coordone
        for elem in [(x + 1, y), (x + 1,y+1), (x+ 1, y -1), (x - 1, y), (x - 1, y - 1), (x - 1, y + 1),
                     (x, y - 1), (x, y + 1)]:
            if not fct.out_of_board(elem) :
                continue
            if self.echiquier.echiquier[elem[0]][elem[1]] is None or self.echiquier.echiquier[elem[0]][elem[1]].couleur != self.couleur:
                ajoute_coup_pas_echec(self,elem,self.echiquier,roi=True,calcul=calcul)
        if not self.premier_coup or self.coordone[0] != 4:
            print("ehin .?")
            return
        if check_ligne_vide(x,x-4,y,self.echiquier.echiquier) and self.echiquier.echiquier[x-4][y] is not None and self.echiquier.echiquier[x-4][y].premier_coup:
            ajoute_coup_pas_echec(self, (x-2,y), self.echiquier, roi=True, calcul=calcul)
        if check_ligne_vide(x,x+3,y,self.echiquier.echiquier) and self.echiquier.echiquier[x+3][y] is not None and self.echiquier.echiquier[x+3][y].premier_coup:
            ajoute_coup_pas_echec(self, (x + 2, y), self.echiquier, roi=True, calcul=calcul)

def check_ligne_vide(x1,x2,y,echiquier):
    sens = -1 if x2-x1<0 else 1
    for i in range(1,abs(x2-x1)):
        if echiquier[x1+i*sens][y] is not None :
            return False
    return True

def calcul_coup_vecteur(piece : Piece,echiquier,vecteur,calcul):
    x,y = piece.coordone
    i ,j = vecteur
    ind = 1
    while True :

        if not fct.out_of_board((x+i*ind,y+j*ind)):
            break
        elif not echiquier.echiquier[x+i*ind][y+j*ind] is None and echiquier.echiquier[x+i*ind][y+j*ind].visible :
            if echiquier.echiquier[x+i*ind][y+j*ind].couleur != piece.couleur :
                ajoute_coup_pas_echec(piece,(x+i*ind,y+j*ind),echiquier, calcul=calcul)
            break
        else :
            ajoute_coup_pas_echec(piece, (x + i * ind, y + j * ind), echiquier, calcul=calcul)
            ind += 1



class PieceImaginaire:
    def __init__(self):
        self.piece = 'ima'
        self.couleur = 'pas'
        self.visible = True


def ajoute_coup_pas_echec(piece: Piece, coordonne, echiquier ,roi=False, calcul=True):

    if not calcul:
        piece.coup.append(coordonne)
        return

    x, y = coordonne
    piece.visible = False
    if echiquier.echiquier[x][y] is None:
        pieceima = PieceImaginaire()
        echiquier.echiquier[x][y] = pieceima
    else:
        couleur = echiquier.echiquier[x][y].couleur
        echiquier.piece_dic[couleur].remove(echiquier.echiquier[x][y])
        echiquier.echiquier[x][y].couleur = 'pas'
        echiquier.echiquier[x][y].peut_jouer = False

    L_coup = piece.echiquier.calcul_all_coup(fct.autre_couleur(piece.couleur) ,roi_mouv=False, calcul=False)
    co_roi = echiquier.roi[piece.couleur].coordone

    if echiquier.echiquier[x][y].piece == 'ima':
        echiquier.echiquier[x][y] = None
        del (pieceima)
    else:
        echiquier.echiquier[x][y].couleur = couleur
        echiquier.echiquier[x][y].peut_jouer = True
        echiquier.piece_dic[couleur].append(echiquier.echiquier[x][y])

    piece.visible = True

    if roi:
        if coordonne in L_coup:
            return
    elif co_roi in L_coup:
        return
    piece.coup.append(coordonne)


