from data import sftp
from events import event_handler
from broadcast import broadcast
from server_ui import server_ui


def handle_connect_client(client):
    connection_message = sftp.connection_message(client.name)
    packet = sftp.send_data(connection_message)
    broadcast(packet)


def handle_disconnect_client(client):
    disconnection_message = sftp.disconnection_message(client.name)
    packet = sftp.send_data(disconnection_message)
    broadcast(packet)


def handle_message(message):
    packet = sftp.send_data(message)
    broadcast(packet)


def setup_broadcast_event_handlers():
    event_handler.subscribe("connect-client", handle_connect_client)
    event_handler.subscribe("disconnect-client", handle_disconnect_client)
    event_handler.subscribe("message", handle_message)
