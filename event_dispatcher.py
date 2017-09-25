import sdl2


class EventDispatcher:
    TIMER_EVENT = 0x8001
    TIMER_INTERVAL = 2

    def __init__(self, event_loop, window):
        self._window = window
        self._event_loop = event_loop
        self._event_dispatchers = {
            sdl2.SDL_WINDOWEVENT: self._dispatch_window_event,
            sdl2.SDL_QUIT: self._dispatch_quit_event,
            sdl2.SDL_MOUSEMOTION: self._dispatch_mouse_event,
            sdl2.SDL_MOUSEBUTTONDOWN: self._dispatch_mouse_event,
            sdl2.SDL_MOUSEBUTTONUP: self._dispatch_mouse_event,
            EventDispatcher.TIMER_EVENT: self._dispatch_timer_event
        }

        # def callback(interval, params):
        #     event = sdl2.SDL_Event()
        #     event.type = sdl2.SDL_USEREVENT
        #     event_pointer = ctypes.byref(event)
        #     sdl2.SDL_PushEvent(event_pointer)
        #     return interval
        #
        # sdl2.SDL_AddTimer(EventDispatcher.TIMER_INTERVAL,
        #                   sdl2.SDL_TimerCallback(callback), None)

    def dispatch(self, event):
        dispatcher = self._event_dispatchers.get(event.type)
        if dispatcher is not None:
            dispatcher(event)

    def _dispatch_window_event(self, event):
        if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
            self._window.resize()

    def _dispatch_mouse_event(self, event):
        if event.motion.type == sdl2.SDL_MOUSEBUTTONDOWN:
            position = event.motion.x, event.motion.y
            self._window.on_mouse_down(position)
        elif event.motion.type == sdl2.SDL_MOUSEBUTTONUP:
            position = event.motion.x, event.motion.y
            self._window.on_mouse_up(position)
        elif event.motion.type == sdl2.SDL_MOUSEMOTION:
            vector = event.motion.xrel, event.motion.yrel
            position = event.motion.x, event.motion.y
            self._window.on_mouse_move(position, vector)

    def _dispatch_timer_event(self, _):
        self._window.timer_tick()

    def _dispatch_quit_event(self, _):
        self._event_loop.stop()
        self._window.close()
