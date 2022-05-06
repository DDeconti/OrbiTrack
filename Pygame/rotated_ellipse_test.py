import pygame
import test

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

def draw_rect_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def draw_ellipse_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

angle = 00
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window_center = window.get_rect().center

    window.fill((255, 255, 255))
    draw_rect_angle(window, (0, 0, 0), (75, 150, 250, 100), angle, 2)
    draw_ellipse_angle(window, (0, 0, 0), (75, 150, 250, 100), angle, 2)
    angle += 1
    pygame.display.flip()

pygame.quit()
exit()