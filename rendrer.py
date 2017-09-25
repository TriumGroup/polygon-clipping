import sdl2

from circle import Circle
from polygon import Polygon


class Renderer:
    WHITE_COLOR = (255, 255, 255, 255)
    BLACK_COLOR = (0, 0, 0, 255)
    VIEWPORT_PADDING = 10
    WIDTH = 1000
    HEIGHT = 700
    VIEWPORT_POINTS = [
        (VIEWPORT_PADDING, VIEWPORT_PADDING),
        (WIDTH - VIEWPORT_PADDING, VIEWPORT_PADDING),
        (WIDTH - VIEWPORT_PADDING, HEIGHT - VIEWPORT_PADDING),
        (VIEWPORT_PADDING, HEIGHT - VIEWPORT_PADDING)
    ]
    INITIAL_RECTANGLE_POINTS = [(250, 250), (450, 250), (450, 450), (250, 450)]
    INITIAL_CIRCLE_PARAMETERS = ((600, 350), 100)

    def __init__(self, window):
        self._window = window
        self.sdl_renderer = sdl2.SDL_CreateRenderer(
            self._window.sdl_window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED
        )
        self._shapes = [
            Polygon(self.sdl_renderer, Renderer.VIEWPORT_POINTS),
            Polygon(self.sdl_renderer, Renderer.INITIAL_RECTANGLE_POINTS),
            Circle(self.sdl_renderer, *Renderer.INITIAL_CIRCLE_PARAMETERS)
        ]

    @property
    def size(self):
        return self._window.size

    def _draw_shapes(self):
        self._clear_draw_field()
        for shape in self._shapes:
            shape.draw()
        self._present_render()

    def resize(self):
        self._draw_shapes()

    def mouse_move(self, position, vector, pressed):
        if pressed:
            if self._shapes[1].contains(position):
                self._shapes[1] = self._shapes[1].move(vector)
            if self._shapes[2].contains(position):
                self._shapes[2] = self._shapes[2].move(vector)
            self._draw_shapes()

    def _clear_draw_field(self):
        sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *self.WHITE_COLOR)
        sdl2.SDL_RenderClear(self.sdl_renderer)
        sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, *self.BLACK_COLOR)

    def _present_render(self):
        sdl2.SDL_RenderPresent(self.sdl_renderer)
