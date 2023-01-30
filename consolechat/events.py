__all__ = ['event_handler']


class _EventHandler:
    def __init__(self):
        self._subscribers = dict()

    def subscribe(self, event_type: str, fn) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(fn)

    def post_event(self, event_type: str, data) -> None:
        if event_type not in self._subscribers:
            return
        for fn in self._subscribers[event_type]:
            fn(data)


event_handler = _EventHandler()
