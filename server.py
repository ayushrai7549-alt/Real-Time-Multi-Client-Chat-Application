#!/usr/bin/env python3
"""
Real-time Chat Server (Beginner Tier)
Tech Stack: Python, socket, threading

Features:
- Listens for incoming client connections on TCP socket.
- Handles multiple concurrent clients using threading.
- Relays messages between connected clients in real time.
- Formats messages with timestamps (e.g., [14:35] Alice: Hello).
- Gracefully handles client disconnections and notifies remaining peers.
- Supports clean shutdown via SIGINT / Ctrl+C.
"""

import socket
import threading
import sys
import argparse
from datetime import datetime

# Default configuration
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
BUFFER_SIZE = 1024

# Thread-safe storage for connected clients: {client_socket: username}
clients_lock = threading.Lock()
clients = {}


def get_timestamp() -> str:
    """Return the current time formatted as HH:MM."""
    return datetime.now().strftime("%H:%M")


def broadcast(message: str, sender_socket: socket.socket = None):
    """
    Broadcast a message to all connected clients except the sender.
    Dead sockets are collected and cleaned up safely.
    """
    formatted_payload = (message + "\n").encode("utf-8")
    dead_sockets = []

    with clients_lock:
        for client_sock in list(clients.keys()):
            if client_sock != sender_socket:
                try:
                    client_sock.sendall(formatted_payload)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    dead_sockets.append(client_sock)

        for dead_sock in dead_sockets:
            dead_user = clients.pop(dead_sock, None)
            try:
                dead_sock.close()
            except OSError:
                pass
            if dead_user:
                print(f"[{get_timestamp()}] [SERVER] Cleaned up disconnected client: {dead_user}")


def handle_client(client_socket: socket.socket, client_address):
    """
    Handle a single client connection throughout its lifecycle.
    Runs inside a dedicated thread per connected client.
    """
    username = None
    buffer = ""

    try:
        # Step 1: Handshake - receive the username from the client
        while "\n" not in buffer:
            chunk = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if not chunk:
                # Connection dropped before sending username
                client_socket.close()
                return
            buffer += chunk

        raw_username, buffer = buffer.split("\n", 1)
        username = raw_username.strip()

        if not username:
            username = f"User-{client_address[1]}"

        # Step 2: Register client
        with clients_lock:
            # Ensure unique display name if needed
            existing_names = set(clients.values())
            base_name = username
            counter = 1
            while username in existing_names:
                username = f"{base_name}_{counter}"
                counter += 1

            clients[client_socket] = username

        # Send confirmation/welcome to the client
        welcome_msg = (
            f"[{get_timestamp()}] [SYSTEM] Welcome to the chat, {username}!\n"
            f"[{get_timestamp()}] [SYSTEM] Type your messages and press Enter. Type '/quit' to exit.\n"
        )
        client_socket.sendall(welcome_msg.encode("utf-8"))

        # Notify other connected clients
        join_notification = f"[{get_timestamp()}] [SYSTEM] {username} has joined the chat."
        print(f"[{get_timestamp()}] [SERVER] {username} connected from {client_address[0]}:{client_address[1]}")
        broadcast(join_notification, sender_socket=client_socket)

        # Step 3: Message receive loop
        while True:
            if "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                message = line.strip()

                if not message:
                    continue

                if message == "/quit":
                    break

                # Timestamped message format: [HH:MM] Username: Message
                timestamped_msg = f"[{get_timestamp()}] {username}: {message}"
                print(f"[{get_timestamp()}] [CHAT] {username}: {message}")
                broadcast(timestamped_msg, sender_socket=client_socket)
            else:
                chunk = client_socket.recv(BUFFER_SIZE).decode("utf-8")
                if not chunk:
                    # Client closed socket connection
                    break
                buffer += chunk

    except (ConnectionResetError, BrokenPipeError):
        pass
    except Exception as e:
        print(f"[{get_timestamp()}] [SERVER ERROR] Error handling client {username or client_address}: {e}")
    finally:
        # Step 4: Graceful cleanup and disconnection notification
        with clients_lock:
            if client_socket in clients:
                del clients[client_socket]

        try:
            client_socket.close()
        except OSError:
            pass

        if username:
            leave_notification = f"[{get_timestamp()}] [SYSTEM] {username} has left the chat."
            print(f"[{get_timestamp()}] [SERVER] {username} disconnected.")
            broadcast(leave_notification)


def start_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    """
    Bind and listen on the given host/port, accepting clients in a loop.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable SO_REUSEADDR so port can be immediately rebound on restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
    except OSError as err:
        print(f"[{get_timestamp()}] [FATAL] Could not bind to {host}:{port} - {err}")
        sys.exit(1)

    server_socket.listen(5)
    print("=" * 60)
    print(f"[*] Real-time Chat Server running on {host}:{port}")
    print(f"[*] Started at: {get_timestamp()}")
    print("[*] Press Ctrl+C to shut down the server gracefully.")
    print("=" * 60)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            client_thread.start()
    except KeyboardInterrupt:
        print(f"\n[{get_timestamp()}] [SERVER] Shutting down server gracefully...")
    finally:
        # Notify all connected clients of server shutdown
        shutdown_msg = f"[{get_timestamp()}] [SYSTEM] Server is shutting down. Connection closed."
        broadcast(shutdown_msg)

        with clients_lock:
            for s in list(clients.keys()):
                try:
                    s.close()
                except OSError:
                    pass
            clients.clear()

        try:
            server_socket.close()
        except OSError:
            pass

        print(f"[{get_timestamp()}] [SERVER] Server stopped.")


def parse_arguments():
    """Parse command line arguments for server host and port."""
    parser = argparse.ArgumentParser(description="Real-Time CLI Chat Server (Beginner Tier)")
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"IP address or hostname to bind server (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port number to listen on (default: {DEFAULT_PORT})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    start_server(host=args.host, port=args.port)
