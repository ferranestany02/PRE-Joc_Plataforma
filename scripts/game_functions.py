import sys
import pygame


def check_key_events(event, movement, music, player):

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            movement[0] = True
        if event.key == pygame.K_RIGHT:
            movement[1] = True
        if event.key == pygame.K_UP:
            if player.jump():
                music.play()
        if event.key == pygame.K_x:
            player.dash()
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            movement[0] = False
        if event.key == pygame.K_RIGHT:
            movement[1] = False

            
def check_events(movement, music, player):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            check_key_events(event, movement, music, player)