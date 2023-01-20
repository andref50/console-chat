class Logger:
    def __init__(self, max_events=100):

        # log a history of "max_events" last events
        self._max_log_events = max_events
        self._log_events = list()

    def log_event(self, event):
        if len(self._log_events) == self._max_log_events:
            self._log_events.pop(0)
        self._log_events.append(event)

    @property
    def get_log_events(self):
        return self._log_events

