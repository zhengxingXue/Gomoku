import pygame
from pygame_widgets import ButtonArray

pygame.init()
win = pygame.display.set_mode((600, 600))

buttonArray = ButtonArray(win, 50, 50, 500, 500, (2, 2),
                          border=100, texts=('1', '2', '3', '4')
                          )

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    buttonArray.listen(events)
    buttonArray.draw()

    pygame.display.update()