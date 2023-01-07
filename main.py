import pygame
import math
from time import time
from GameBoard import Node, Graph, GRAY, END, GREEN, RED, INSTRUCTION

width = 800  # Width of the window
height = width  # Height of the Window matches the width
boxSize = width / 10  # Sets the size of the collision box and image to 1/10th of the window size

pygame.init()
playing = True

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('462 Node Connecting Final')  # Window title

current_location = [-boxSize, -boxSize]

# everything inside rendering list will be render to the screen
sprites: list[Node] = []

# game clock, use to set max fps
clock = pygame.time.Clock()

# create 100 sprites and putting them at apropriate locations
id = -1
block = []

# columns
for _ in range(0, 10):
    current_location[1] += boxSize
    current_location[0] = -boxSize
    # rows
    for _ in range(0, 10):
        id += 1

        if 0 <= id <= 9:
            block.append(0)
        if id % 10 == 0:
            block.append(3)
        if (id - 9) % 10 == 0:
            block.append(1)
        if 90 <= id <= 99:
            block.append(2)

        current_location[0] += boxSize

        if id == 0:
            node = Node(id, GREEN, tuple(current_location), (boxSize, boxSize), tuple(block))
        elif id == 99:
            node = Node(id, END, tuple(current_location), (boxSize, boxSize), (1, 2, 3))
        else:
            node = Node(id, GRAY, tuple(current_location), (boxSize, boxSize), tuple(block))

        sprites.append(node)
        block = []

# render objects
rendering = pygame.sprite.RenderPlain(sprites)
graph = Graph(100)

# Add all the connections here.
for i in sprites:
    graph.addConnection(i, sprites)

# update image at least once
graph.updateImage(sprites)

victory = False
instruction = True
def draw_Inst():
    inst = pygame.transform.scale(INSTRUCTION, (800, 448))
    screen.blit(inst,(0,0))
start_counter = time()
while playing:
    # 144 max fps
    clock.tick(144)
    # check for events
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            playing = False

        # check mouse event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if instruction: # If the instruction page is up, close the page and start the time
                instruction = False
                start_counter = time()
            else:
            # get location where the mouse clicked
                x, y = event.pos
                for node in sprites:
                # check which sprite did the player clicked and rotate it clockwise
                    if node.rect.collidepoint(x, y):
                        node.changeRotation(1)
                        graph.addConnection(node, sprites)
                        graph.updateImage(sprites)

                if graph.checkVictory(sprites[0], sprites[-1]):
                    playing = False
                    victory = True

    # draw all the sprites on the screen
    rendering.draw(screen)
    if instruction:
        draw_Inst()

    pygame.display.update()

end_counter = time()

def draw_Inst():
    inst = pygame.transform.scale(INSTRUCTION, (800, 448))
    screen.blit(inst,(0,0))

def draw_text(txt, font_size, padx, pady, width, screen, position, color=(0, 0, 0), bg=(0, 0, 0)):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    space = font.size(' ')[0]
    text_array = [word.split(' ') for word in txt.splitlines()]
    x, y = position

    for line in text_array:
        for word in line:
            text = font.render(word, 1, color, bg)
            text_w, text_h = text.get_size()
            if x + text_w >= width:
                x = position[0]
                y += text_h

            x += padx if x == 0 else 0
            y += pady if y == 0 else 0

            screen.blit(text, (x, y))
            x += text_w + space

        x = position[0]
        y += text_h


if victory == True:
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    X = 400
    Y = 400

    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('Victory!')
    # font = pygame.font.Font('freesansbold.ttf', 32)
    # text = font.render(f"You Win!", True, green, blue)
    # textRect = text.get_rect()
    # textRect.center = (X // 2, Y // 2)

    while True:
        display_surface.fill(blue)
        # display_surface.blit(text, textRect)
        draw_text(f"You Win!",
                  20, 0, 0, 5000, display_surface, (X / 2.5, Y // 3), green)

        draw_text(f"\n\nYou Completed it in: {round(end_counter - start_counter, 2)} Seconds",
                  20, 0, 0, 5000, display_surface, (X // 10, Y // 3), green)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()

pygame.quit()