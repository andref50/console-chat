from events import event_handler

from server_ui import server_ui


def handle_connect_client(*args):
    server_ui.update()


def handle_disconnect_client(*args):
    server_ui.update()


def handle_message(*args):
    server_ui.update()


def setup_ui_event_handlers():
    event_handler.subscribe("connect-client", handle_connect_client)
    event_handler.subscribe("disconnect-client", handle_disconnect_client)
    event_handler.subscribe("message", handle_message)
