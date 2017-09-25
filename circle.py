from math import hypot
from random import randrange

import sdl2

from helper import line_contains
from shape import Shape


class Circle(Shape):
    def __init__(self, sdl_renderer, center, radius, is_point_visible=Shape.ALWAYS_VISIBLE,
                 dash_length=Shape.DEFAULT_DASH_LENGTH, viewport_points=None):
        self._viewport_edges = viewport_points
        self._is_point_visible = is_point_visible
        self._sdl_renderer = sdl_renderer
        self._center_x, self._center_y = center
        self._radius = radius
        self._dash_length = dash_length

    def draw(self):
        x = 0
        y = self._radius
        delta = 1 - 2 * self._radius
        point_index = 0
        while y >= 0:
            self._draw_circle_points(x, y, point_index)
            point_index += 1
            error = 2 * (delta + y) - 1
            if (delta < 0) and (error <= 0):
                x += 1
                delta += 2 * x + 1
                continue
            error = 2 * (delta - x) - 1
            if (delta > 0) and (error > 0):
                y -= 1
                delta += 1 - 2 * y
                continue
            x += 1
            delta += 2 * (x - y)
            y -= 1

    def rotate(self, angle):
        return self

    def move(self, vector):
        delta_x, delta_y = vector
        return Circle(self._sdl_renderer, (self._center_x + delta_x, self._center_y + delta_y), self._radius,
                      self._is_point_visible, self._dash_length, self._viewport_edges)

    def contains(self, point):
        x, y = point
        return hypot(x - self._center_x, y - self._center_y) <= self._radius

    def _draw_circle_points(self, x, y, point_index):
        self._draw_point(self._center_x + x, self._center_y + y, point_index)
        self._draw_point(self._center_x + x, self._center_y - y, point_index)
        self._draw_point(self._center_x - x, self._center_y + y, point_index)
        self._draw_point(self._center_x - x, self._center_y - y, point_index)

    def _is_draw_dash_point(self, point_index):
        return point_index % (self._dash_length * 2) > self._dash_length

    def _draw_point(self, x, y, point_index):
        if self._is_point_visible((x, y)):
            sdl2.SDL_RenderDrawPoint(self._sdl_renderer, x, y)
        else:
            if self._is_draw_dash_point(point_index):
                sdl2.SDL_RenderDrawPoint(self._sdl_renderer, x, y)

    def edge_vector(self):
        top = (self._center_x, self._center_y - self._radius)
        bottom = (self._center_x, self._center_y + self._radius)
        left = (self._center_x - self._radius, self._center_y)
        right = (self._center_x + self._radius, self._center_y)
        if line_contains(*self._viewport_edges[0], top):
            return randrange(-1, 1), 1
        elif line_contains(*self._viewport_edges[1], right):
            return -1, randrange(-1, 1)
        elif line_contains(*self._viewport_edges[2], bottom):
            return randrange(-1, 1), -1
        elif line_contains(*self._viewport_edges[3], left):
            return 1, randrange(-1, 1)
        else:
            return None
