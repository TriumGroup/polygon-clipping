from math import cos, sin

from line import Line


class Rectangle:
    DEFAULT_DASH_LENGTH = 4

    def __init__(self, sdl_renderer, left_top, right_bottom, is_point_visible, dash_length=DEFAULT_DASH_LENGTH):
        self._is_point_visible = is_point_visible
        self._sdl_renderer = sdl_renderer
        self._left_top = left_top
        self._right_bottom = right_bottom
        self._dash_length = dash_length

    def draw(self):
        x1, y1 = self._left_top
        x2, y2 = self._right_bottom
        self._draw_line((x1, y1), (x2, y1))
        self._draw_line((x2, y1), (x2, y2))
        self._draw_line((x2, y2), (x1, y2))
        self._draw_line((x1, y2), (x1, y1))

    def _draw_line(self, start, end):
        Line(self._sdl_renderer, start, end, self._is_point_visible, self._dash_length)

    def rotate(self, angle):
        x1, y1 = self._left_top
        x2, y2 = self._right_bottom
        center = ((x2 - x1) // 2, (y2 - y1) // 2)
        new_left_top = self._rotate_point(center, x1, y1, angle)
        new_right_bottom = self._rotate_point(center, x1, y1, angle)
        return Rectangle(self._sdl_renderer, new_left_top, new_right_bottom, self._is_point_visible, self._dash_length)

    def _rotate_point(self, rotation_point, x, y, angle):
        center_x, center_y = rotation_point
        rotated_x = center_x + (x - center_x) * cos(angle) - (y - center_y) * sin(angle)
        rotated_y = center_y + (y - center_y) * cos(angle) + (x - center_x) * sin(angle)
        return (rotated_x, rotated_y)
