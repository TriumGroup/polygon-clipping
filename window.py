import ctypes

import sdl2

from rendrer import Renderer


class Window:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600

    def __init__(self, title, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_TIMER)
        self.sdl_window = sdl2.SDL_CreateWindow(
            title,
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            width,
            height,
            sdl2.SDL_WINDOW_RESIZABLE
        )
        self._right_mouse_pressed = False
        self._left_mouse_pressed = False
        self._renderer = Renderer(self)
        self.resize()

    @property
    def size(self):
        width = ctypes.c_int()
        height = ctypes.c_int()
        sdl2.SDL_GetWindowSize(self.sdl_window, ctypes.byref(width), ctypes.byref(height))
        return width.value, height.value

    def on_rotate(self):
        self._renderer.on_rotate()

    def resize(self):
        self._renderer.resize()

    def on_mouse_down(self, position, is_left):
        if is_left:
            self._left_mouse_pressed = True
        else:
            self._right_mouse_pressed = True

    def on_mouse_up(self, position, is_left):
        if is_left:
            self._left_mouse_pressed = False
        else:
            self._right_mouse_pressed = False

    def on_circle_event(self):
        self._renderer.on_circle_event()

    @property
    def can_rotate(self):
        return self._right_mouse_pressed

    def on_mouse_move(self, position, vector):
        self._renderer.mouse_move(position, vector, self._left_mouse_pressed)

    def close(self):
        sdl2.SDL_DestroyWindow(self.sdl_window)
        sdl2.SDL_Quit()
