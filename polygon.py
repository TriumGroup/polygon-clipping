from helper import pairs, centroid, rotate_point

from line import Line
from shape import Shape


class Polygon(Shape):
    DEFAULT_DASH_LENGTH = 4

    def __init__(self, sdl_renderer, points, is_point_visible=lambda point: True, dash_length=DEFAULT_DASH_LENGTH):
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

    def move(self, vector):
        def move_point(point, vector):
            x, y = point
            delta_x, delta_y = vector
            return x + delta_x, y + delta_y

        new_points = [*map(lambda point: move_point(point, vector), self._points)]
        return Polygon(self._sdl_renderer, new_points, self._is_point_visible, self._dash_length)

    def contains(self, point):
        x, y = point
        RIGHT = "RIGHT"
        LEFT = "LEFT"

        def inside_convex_polygon(point, vertices):
            previous_side = None
            n_vertices = len(vertices)
            for n in range(n_vertices):
                a, b = vertices[n], vertices[(n + 1) % n_vertices]
                affine_segment = v_sub(b, a)
                affine_point = v_sub(point, a)
                current_side = get_side(affine_segment, affine_point)
                if current_side is None:
                    return False  # outside or over an edge
                elif previous_side is None:  # first segment
                    previous_side = current_side
                elif previous_side != current_side:
                    return False
            return True

        def get_side(a, b):
            x = x_product(a, b)
            if x < 0:
                return LEFT
            elif x > 0:
                return RIGHT
            else:
                return None

        def v_sub(a, b):
            return a[0] - b[0], a[1] - b[1]

        def x_product(a, b):
            return a[0] * b[1] - a[1] * b[0]

        return inside_convex_polygon((x, y), self._points)
