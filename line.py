from math import trunc

import sdl2

from helper import move_point, centroid, rotate_point, line_contains
from shape import Shape


# Attention! Optimized code below! Take care of your eyes.
class Line(Shape):
    def __init__(self, sdl_renderer, start, end, is_point_visible=Shape.ALWAYS_VISIBLE,
                 dash_length=Shape.DEFAULT_DASH_LENGTH):
        self._is_point_visible = is_point_visible
        self._sdl_renderer = sdl_renderer
        self._dash_length = dash_length
        x1, y1, x2, y2 = tuple(map(trunc, start + end))
        self._start = (x1, y1)
        self._end = (x2, y2)
        self._delta_x = abs(x2 - x1)
        self._delta_y = abs(y2 - y1)
        self._step_x = 1 if x2 >= x1 else -1
        self._step_y = 1 if y2 >= y1 else -1
        self._d2 = -abs(self._delta_x - self._delta_y) * 2

    def draw(self):
        if self._delta_x >= self._delta_y:
            self._draw_by_continuous_x_increase(self._start)
        else:
            self._draw_by_continuous_y_increase(self._start)

    def rotate(self, angle):
        center = centroid(self._start, self._end)
        return Line(self._sdl_renderer,
                    rotate_point(center, self._start, angle), rotate_point(center, self._end, angle),
                    self._is_point_visible, self._dash_length)

    def contains(self, point):
        return line_contains(self._start, self._end, point)

    def move(self, vector):
        return Line(self._sdl_renderer,
                    move_point(self._start, vector), move_point(self._end, vector),
                    self._is_point_visible, self._dash_length)

    def _draw_by_continuous_x_increase(self, start):
        x, y = start
        d1 = self._delta_y * 2
        d = d1 - self._delta_x
        point_index = 0
        for i in range(self._delta_x):
            self._draw_point(x, y, point_index)
            point_index += 1
            x += self._step_x
            if d > 0:
                d += self._d2
                y += self._step_y
            else:
                d += d1

    def _draw_by_continuous_y_increase(self, start):
        x, y = start
        d1 = self._delta_x * 2
        d = d1 - self._delta_y
        point_index = 0
        for i in range(self._delta_y):
            self._draw_point(x, y, point_index)
            point_index += 1
            y += self._step_y
            if d > 0:
                d += self._d2
                x += self._step_x
            else:
                d += d1

    def _is_draw_dash_point(self, point_index):
        return point_index % (self._dash_length * 2) > self._dash_length

    def _draw_point(self, x, y, point_index):
        if self._is_point_visible((x, y)):
            sdl2.SDL_RenderDrawPoint(self._sdl_renderer, x, y)
        else:
            if self._is_draw_dash_point(point_index):
                sdl2.SDL_RenderDrawPoint(self._sdl_renderer, x, y)
