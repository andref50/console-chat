from events import event_handler
from logger import log
from data import sftp


def handle_connect_client(client):
    connection_message = sftp.connection_message(client.name)
    log.log_event(connection_message)


def handle_disconnect_client(client):
    disconnection_message = sftp.disconnection_message(client.name)
    log.log_event(disconnection_message)


def handle_message(message):
    log.log_event(message)


def setup_log_event_handlers():
    event_handler.subscribe("connect-client", handle_connect_client)
    event_handler.subscribe("disconnect-client", handle_disconnect_client)
    event_handler.subscribe("message", handle_message)
