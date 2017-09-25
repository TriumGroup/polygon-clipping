from math import radians

import sdl2

from circle import Circle
from polygon import Polygon


class Renderer:
    ONE_DEGREE = radians(3)
    WHITE_COLOR = (255, 255, 255, 255)
    BLACK_COLOR = (0, 0, 0, 255)
    VIEWPORT_PADDING = 100
    WIDTH = 600
    HEIGHT = 600
    VIEWPORT_POINTS = [
        (VIEWPORT_PADDING, VIEWPORT_PADDING),
        (WIDTH - VIEWPORT_PADDING, VIEWPORT_PADDING),
        (WIDTH - VIEWPORT_PADDING, HEIGHT - VIEWPORT_PADDING),
        (VIEWPORT_PADDING, HEIGHT - VIEWPORT_PADDING)
    ]
    INITIAL_RECTANGLE_POINTS = [(150, 325), (450, 325), (450, 375), (150, 375)]
    INITIAL_CIRCLE_PARAMETERS = ((600, 350), 100)

    def __init__(self, window):
        self._window = window
        self.sdl_renderer = sdl2.SDL_CreateRenderer(
            self._window.sdl_window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED
        )
        self._viewport = Polygon(self.sdl_renderer, Renderer.VIEWPORT_POINTS)
        rectangle = Polygon(self.sdl_renderer, Renderer.INITIAL_RECTANGLE_POINTS,
                            is_point_visible=self._viewport.contains)

        self._shapes = [
            rectangle,
            Circle(self.sdl_renderer, *Renderer.INITIAL_CIRCLE_PARAMETERS,
                   lambda point: self._viewport.contains(point) and not self._shapes[0].contains(point))
        ]

    @property
    def size(self):
        return self._window.size

    def _draw_shapes(self):
        self._clear_draw_field()
        self._viewport.draw()
        for shape in self._shapes:
            shape.draw()
        self._present_render()

    def resize(self):
        self._draw_shapes()

    def mouse_move(self, position, vector, pressed):
        if pressed:
            for index, shape in enumerate(self._shapes):
                if shape.contains(position):
                    self._shapes[index] = shape.move(vector)
            self._draw_shapes()

    def timer_tick(self):
        self._shapes = [*map(lambda shape: shape.rotate(Renderer.ONE_DEGREE), self._shapes)]
        self._draw_shapes()

    def _clear_draw_field(self):
        sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *self.WHITE_COLOR)
        sdl2.SDL_RenderClear(self.sdl_renderer)
        sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *self.BLACK_COLOR)

    def _present_render(self):
        sdl2.SDL_RenderPresent(self.sdl_renderer)
