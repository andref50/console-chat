from events import event_handler
from client_ui import client_ui


def handle_connect_client(*args):
    client_ui._update()


def handle_disconnect_client(*args):
    client_ui._update()


def handle_message(*args):
    client_ui._update()


def setup_ui_event_handlers():
    event_handler.subscribe("connect-client", handle_connect_client)
    event_handler.subscribe("disconnect-client", handle_disconnect_client)
    event_handler.subscribe("message", handle_message)
