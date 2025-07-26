import pygame
from utilitaire import constante as cst
from game import Game

running = True


pygame.time.set_timer(cst.PASSESECONDE, 1000)
# pygame.time.set_timer(changecouleur, 250)

game = Game()

while running :
    cst.screen.fill((50,50,50))
    game.boucle()
    game.afficher(cst.screen)
    for event in pygame.event.get():
        game.event(event)
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                running = False
                pygame.quit()

    if running:
        pygame.display.flip()