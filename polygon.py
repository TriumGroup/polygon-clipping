from helper import pairs, centroid, rotate_point, move_point

from line import Line
from shape import Shape


class Polygon(Shape):
    def __init__(self, sdl_renderer, points, is_point_visible=Shape.ALWAYS_VISIBLE,
                 dash_length=Shape.DEFAULT_DASH_LENGTH):
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
        center = centroid(*self._points)
        new_points = [*map(lambda point: rotate_point(center, point, angle), self._points)]
        return Polygon(self._sdl_renderer, new_points, self._is_point_visible, self._dash_length)

    def move(self, vector):
        new_points = [*map(lambda point: move_point(point, vector), self._points)]
        return Polygon(self._sdl_renderer, new_points, self._is_point_visible, self._dash_length)

    def contains(self, point):
        x, y = point
        RIGHT = 0x1
        LEFT = 0x2

        def inside_convex_polygon(point, vertices):
            previous_side = None
            for first, second in pairs(vertices):
                affine_segment = point_sub(second, first)
                affine_point = point_sub(point, first)
                current_side = get_side(affine_segment, affine_point)
                if current_side is None:
                    return False  # outside or over an edge
                elif previous_side is None:  # first segment
                    previous_side = current_side
                elif previous_side != current_side:
                    return False
            return True

        def get_side(start, end):
            product = x_product(start, end)
            if product < 0:
                return LEFT
            elif product > 0:
                return RIGHT
            else:
                return None

        def point_sub(first, second):
            first_x, first_y = first
            second_x, second_y = second
            return first_x - second_x, first_y - second_y

        def x_product(first, second):
            first_x, first_y = first
            second_x, second_y = second
            return first_x * second_y - first_y * second_x

        return inside_convex_polygon((x, y), self._points)
