__all__ = ['log']


class Logger:
    """
        Logger object class holds all events created by the server.
    """

    def __init__(self, max_events: int = 100) -> None:

        self._max_log_events = max_events
        self._log_events = []

    def log_event(self, event: dict) -> None:
        if len(self._log_events) == self._max_log_events:
            self._log_events.pop(0)
        self._log_events.append(event)

    @property
    def get_log_events(self) -> list:
        return self._log_events

    def __len__(self) -> int:
        return len(self._log_events)

    def __repr__(self) -> str:
        return f"Logger({self._max_log_events = }, {len(self._log_events) = }"


log = Logger(max_events=100)
