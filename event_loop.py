import ctypes

import sdl2

from event_dispatcher import EventDispatcher


class EventLoop:
    def __init__(self, window):
        self._event_dispatcher = EventDispatcher(self, window)
        self._running = False

        rotate_event = sdl2.SDL_Event()
        rotate_event.type = EventDispatcher.ROTATE_EVENT
        self._window = window
        self._rotate_event_pointer = ctypes.byref(rotate_event)

        circle_event = sdl2.SDL_Event()
        circle_event.type = EventDispatcher.CIRCLE_EVENT
        self._window = window
        self._circe_event_pointer = ctypes.byref(circle_event)

    def run(self):
        self._running = True
        while self._running:
            if self._window.can_rotate:
                sdl2.SDL_PushEvent(self._rotate_event_pointer)
            sdl2.SDL_PushEvent(self._circe_event_pointer)
            self._receive_events()

    def stop(self):
        self._running = False

    def _receive_events(self):
        event = sdl2.SDL_Event()
        event_pointer = ctypes.byref(event)
        while self._running and sdl2.SDL_PollEvent(event_pointer) != 0:
            self._event_dispatcher.dispatch(event)
