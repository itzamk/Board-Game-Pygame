import random
import pygame
from pygame import Surface
from pygame.sprite import Sprite

GREEN = pygame.image.load("Green.png")
GRAY = pygame.image.load("Gray.png")
END = pygame.image.load("End.png")
RED = pygame.image.load("Red.png")
INSTRUCTION = pygame.image.load("instructions.png")


class Node(Sprite):
    def __init__(self, id: int, image: Surface, xy: tuple[float, float], scale: tuple[float, float],
                 block_rotatation: tuple[int]) -> None:
        super().__init__()
        self.id = id
        self._rotation = random.randint(1, 4)
        self._block_rotation = block_rotatation
        # screen = pygame.display.get_surface()
        self._scale = scale
        self._image = pygame.transform.scale(image.convert(), self._scale)
        self.changeRotation(1)
        self.rect = self.image.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]

    def __str__(self) -> str:
        return f"Node {self.id}"

    def __repr__(self) -> str:
        return self.__str__()

    def changeRotation(self, direction: int):
        '''if direction is a positive number or zero, the sprite will rotate clock wise\n
        if direction is a negative number, the sprite will rotate anti-clock wise'''

        direction = 1 if direction >= 0 else -1

        # do while loop work around because python don't have do while loop
        while True:
            self._rotation = (self._rotation + direction) % 4
            if self._rotation not in self._block_rotation:
                break

        self.image = pygame.transform.rotate(self._image, -90 * self._rotation)

        return self._rotation

    def getRotation(self):
        '''0 look up\n
        1 look right\n
        2 look down\n
        3 look left'''
        return self._rotation

    def changeImage(self, image: Surface):
        self._image = pygame.transform.scale(image.convert(), self._scale)
        self.image = pygame.transform.rotate(self._image, -90 * self._rotation)


class Graph:
    def __init__(self, num_of_nodes):
        self.nodes = num_of_nodes
        self.g_dict: dict[Node: Node] = {}

    # def _addEdge(self, u, v):
    #     if v not in self.g_dict.get(u):
    #         self.g_dict[u].append(v)

    # def _removeEdge(self, u, v):
    #     if v in self.g_dict.get(u):
    #         self.g_dict[u].remove(v)

    def __str__(self) -> str:
        string = "{"
        for k, v in self.g_dict.items():
            string += f"{k} -> {v}, "

        string = string[:-2] + "}"
        return string

    def __repr__(self) -> str:
        return self.__str__()

    def addConnection(self, node: Node, sprites: list[Node]):
        if node.getRotation() == 0:
            self.g_dict[node] = sprites[node.id - 10]
            # self._addEdge(node, node.id - 10)
            # self._removeEdge(node, node.id - 1)
        elif node.getRotation() == 1:
            self.g_dict[node] = sprites[node.id + 1]
            # self._addEdge(node, node.id + 1)
            # self._removeEdge(node, node.id - 10)
        elif node.getRotation() == 2:
            self.g_dict[node] = sprites[node.id + 10]
            # self._addEdge(node, node.id + 10)
            # self._removeEdge(node, node.id + 1)
        elif node.getRotation() == 3:
            self.g_dict[node] = sprites[node.id - 1]
            # self._addEdge(node, node.id - 1)
            # self._removeEdge(node, node.id + 10)

    def updateImage(self, sprites: list[Node]):
        new_item = sprites[0]
        connected_nodes = []

        while new_item not in connected_nodes and new_item.id != 99:
            connected_nodes.append(new_item)
            new_item = self.g_dict[new_item]

        for i in sprites:
            if i in connected_nodes:
                i.changeImage(GREEN)
            elif i.id != 99:
                i.changeImage(GRAY)

    def checkVictory(self, source: Node, destination: Node):
        visited = []

        queue = []
        queue.append(source)
        visited.append(source)

        while queue:
            new: Node = self.g_dict[queue.pop()]
            if new is destination:
                return True

            if new not in visited:
                queue.append(new)
                visited.append(new)

        return False