class Logger:
    def __init__(self, max_events=10, max_log_messages=100):
        # log a history of # last events
        self._max_log_events = max_events
        self._log_events = list()

        # log messages history
        self._max_log_messages = max_log_messages
        self._log_messages = list()

    def log_event(self, event):
        if len(self._log_events) == self._max_log_events:
            self._log_events.pop(0)
        self._log_events.append(event)

    @property
    def get_log_events(self):
        return self._log_events

    def log_message(self, message):
        if len(self._log_messages) == self._max_log_messages:
            self._log_messages.pop(0)
        self._log_messages.append(message)

    @property
    def get_log_messages(self):
        return self._log_messages