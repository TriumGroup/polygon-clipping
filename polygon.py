from helper import pairs, centroid, rotate_point

from line import Line


class Polygon:
    DEFAULT_DASH_LENGTH = 4

    def __init__(self, sdl_renderer, points, is_point_visible=lambda x, y: True, dash_length=DEFAULT_DASH_LENGTH):
        self._is_point_visible = is_point_visible
        self._points = points
        self._sdl_renderer = sdl_renderer
        self._dash_length = dash_length

    def draw(self):
        for first, second in pairs(self._points):
            self._draw_line(first, second)

    def _draw_line(self, start, end):
        Line(self._sdl_renderer, start, end, self._is_point_visible, self._dash_length).draw()

    def rotate(self, angle):
        center = centroid(self._points)
        new_points = [*map(lambda point: rotate_point(center, *point, angle), self._points)]
        return Polygon(self._sdl_renderer, new_points, self._is_point_visible, self._dash_length)
