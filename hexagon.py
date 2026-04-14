import pygame

class Hexagon:
    def __init__(self, points):
        self.points = points

    def draw_move(self, screen):
        pygame.draw.circle(screen, (255, 187, 0), self.get_hexagon_center(), 10)
    def draw_fire(self, screen):
        pygame.draw.circle(screen, (128, 0, 128), self.get_hexagon_center(), 10)
    def contains_point(self, point):
        rect = pygame.Rect(*self.get_hexagon_bounds())
        return rect.collidepoint(*point)

    def get_hexagon_bounds(self):
        min_x = min(point[0] for point in self.points)
        min_y = min(point[1] for point in self.points)
        max_x = max(point[0] for point in self.points)
        max_y = max(point[1] for point in self.points)
        return min_x, min_y, max_x - min_x, max_y - min_y

    def get_hexagon_center(self):
        min_x, min_y, width, height = self.get_hexagon_bounds()
        center_x = min_x + width / 2
        center_y = min_y + height / 2
        return center_x, center_y