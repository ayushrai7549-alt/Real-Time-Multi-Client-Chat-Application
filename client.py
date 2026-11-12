#!/usr/bin/env python3
"""
Real-time Chat Client (Beginner Tier)
Tech Stack: Python, socket, threading

Features:
- Connects to chat server via TCP socket.
- Prompts for username on startup.
- Spawns a background thread to listen for incoming messages in real-time.
- Main thread handles user keyboard input concurrently.
- Formats local messages with timestamp (e.g., [14:35] You: Hello).
- Renders received peer messages with timestamp prefix (e.g., [14:35] Alice: Hello).
- Graceful disconnect handling via '/quit' or Ctrl+C.
"""

import socket
import threading
import sys
import argparse
from datetime import datetime

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
BUFFER_SIZE = 1024


def get_timestamp() -> str:
    """Return the current time formatted as HH:MM."""
    return datetime.now().strftime("%H:%M")


def receive_messages(sock: socket.socket, stop_event: threading.Event):
    """
    Background worker thread function to receive and display messages from server.
    """
    buffer = ""
    try:
        while not stop_event.is_set():
            chunk = sock.recv(BUFFER_SIZE).decode("utf-8")
            if not chunk:
                # Server closed the connection
                if not stop_event.is_set():
                    sys.stdout.write(f"\r\n[{get_timestamp()}] [SYSTEM] Connection closed by server.\n")
                    sys.stdout.flush()
                break

            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                message = line.strip()
                if message:
                    # Clear current line and reprint prompt cleanly
                    sys.stdout.write(f"\r{message}\n> ")
                    sys.stdout.flush()

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        if not stop_event.is_set():
            sys.stdout.write(f"\r\n[{get_timestamp()}] [SYSTEM] Connection lost.\n")
            sys.stdout.flush()
    finally:
        stop_event.set()


def start_client(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, username: str = None):
    """
    Connect to the server and initiate the real-time chat session.
    """
    # Prompt for username if not provided via arguments
    if not username:
        try:
            username = input("Enter your username: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            sys.exit(0)

    while not username:
        print("Username cannot be blank.")
        try:
            username = input("Enter your username: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            sys.exit(0)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
    except (ConnectionRefusedError, OSError) as err:
        print(f"[{get_timestamp()}] [ERROR] Could not connect to server at {host}:{port} - {err}")
        print("Ensure the server is running (python3 server.py).")
        sys.exit(1)

    print("=" * 60)
    print(f"Connected to chat server at {host}:{port} as '{username}'")
    print("Commands:")
    print("  Type any message and press Enter to send.")
    print("  Type '/quit' or press Ctrl+C to exit.")
    print("=" * 60)

    # Handshake: send username to the server
    try:
        client_socket.sendall((username + "\n").encode("utf-8"))
    except OSError as err:
        print(f"[{get_timestamp()}] [ERROR] Failed to send username: {err}")
        client_socket.close()
        sys.exit(1)

    stop_event = threading.Event()

    # Start thread for receiving messages
    recv_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, stop_event),
        daemon=True,
    )
    recv_thread.start()

    # Main thread handles sending messages
    try:
        while not stop_event.is_set():
            try:
                sys.stdout.write("> ")
                sys.stdout.flush()
                user_input = sys.stdin.readline()
                if not user_input:
                    # EOF (e.g. Ctrl+D)
                    break

                message = user_input.strip()
                if not message:
                    continue

                if message == "/quit":
                    # Send /quit to notify the server
                    try:
                        client_socket.sendall(b"/quit\n")
                    except OSError:
                        pass
                    break

                # Display our sent message with timestamp
                timestamp = get_timestamp()
                sys.stdout.write(f"\033[A\r[{timestamp}] You: {message}\n")
                sys.stdout.flush()

                # Send message to server
                client_socket.sendall((message + "\n").encode("utf-8"))

            except (BrokenPipeError, ConnectionResetError):
                print(f"\n[{get_timestamp()}] [SYSTEM] Unable to send message. Disconnected.")
                break

    except KeyboardInterrupt:
        # Graceful handling of Ctrl+C
        pass
    finally:
        stop_event.set()
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            client_socket.close()
        except OSError:
            pass
        print(f"\n[{get_timestamp()}] [SYSTEM] Disconnected from chat. Goodbye!")


def parse_arguments():
    """Parse command line arguments for client connection."""
    parser = argparse.ArgumentParser(description="Real-Time CLI Chat Client (Beginner Tier)")
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Server IP or hostname (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Server port (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--username",
        "-u",
        default=None,
        help="Your username for the chat session",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    start_client(host=args.host, port=args.port, username=args.username)
