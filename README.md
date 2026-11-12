# 💬 Real-Time Multi-Client Chat Application

A real-time client-server messaging application developed using Python TCP sockets and multithreading. It enables multiple users to connect to a centralized server and exchange messages simultaneously through an interactive terminal interface.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Networking](https://img.shields.io/badge/Networking-TCP%20Sockets-orange.svg?style=for-the-badge)
![Concurrency](https://img.shields.io/badge/Concurrency-Multithreading-purple.svg?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Execution Guide](#-execution-guide)
- [Server Configuration](#-server-configuration)
- [Client Commands](#-client-commands)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

The **Real-Time Multi-Client Chat Application** is a lightweight messaging system built using Python's low-level networking capabilities.

It follows a client-server architecture in which a central TCP server manages multiple connected clients and distributes messages between them.

The application uses multithreading to handle concurrent client connections, allowing multiple participants to communicate without blocking one another.

### Architecture

The application consists of two main components:

1. **Server:** Accepts incoming TCP connections, manages connected clients, receives messages, and broadcasts them to active participants.
2. **Client:** Connects to the server, sends messages, and listens for incoming broadcasts.

---

## ✨ Key Features

### 🌐 TCP Client-Server Communication

- Uses TCP sockets for reliable communication.
- Centralized server architecture.
- Supports multiple simultaneous client connections.
- Configurable server host and port.

### ⚡ Multithreaded Architecture

- Dedicated listener thread for each connected client.
- Supports concurrent message handling.
- Allows multiple participants to communicate simultaneously.
- Reduces blocking during message reception.

### 📢 Real-Time Message Broadcasting

- Broadcasts messages to connected participants.
- Thread-safe client management.
- Supports bidirectional communication.
- Automatically timestamps messages.

### 🔄 Connection Management

- Detects client disconnections.
- Cleans up disconnected socket connections.
- Notifies remaining participants when a user leaves.
- Supports graceful client termination.

### 🕒 Timestamped Messaging

Messages are formatted with timestamps using the following format:

```text
[HH:MM] Username: Your message
```

### 📦 Zero External Dependencies

Uses Python's built-in modules:

- `socket`
- `threading`
- `datetime`

No third-party packages are required.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| socket | TCP network communication |
| threading | Concurrent client handling |
| datetime | Message timestamps |
| argparse | Command-line configuration |

---

## 💻 Prerequisites

Before running the application, ensure you have:

- Python 3.10 or higher
- Terminal / Command Prompt
- Git (optional)
- Available network port for server communication

Verify Python installation:

```bash
python --version
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/LAKSHYAMARODIA01/python-projects.git
cd python-projects/chat-application
```

### 2. No Additional Dependencies Required

The application uses Python's standard library, so there is no need to install external packages.

---

## 🎮 Execution Guide

To demonstrate real-time communication, open at least three terminal windows.

### Terminal 1 — Start the Server

```bash
python server.py
```

The server starts on:

```text
Host: 127.0.0.1
Port: 5000
```

Keep this terminal running while clients connect.

### Terminal 2 — Connect Client 1

```bash
python client.py -u Alice
```

### Terminal 3 — Connect Client 2

```bash
python client.py -u Bob
```

Both users can now exchange messages through the server.

### Sample Chat Interaction

**Alice:**

```text
Hello Bob!
```

**Bob:**

```text
Hi Alice! How are you?
```

**Server Broadcast:**

```text
[20:15] Alice: Hello Bob!
[20:15] Bob: Hi Alice! How are you?
```

*Sample output is illustrative.*

---

## ⚙️ Server Configuration

The application supports custom host and port configuration.

### Start Server on a Custom Port

```bash
python server.py --host 0.0.0.0 --port 6000
```

### Connect a Client to the Custom Server

```bash
python client.py --host 127.0.0.1 --port 6000 -u Alice
```

### Command-Line Options

| Option | Description |
|---|---|
| `--host` | Specifies the server IP address |
| `--port` | Specifies the server port |
| `-u` | Sets the client's username |

**Note:** The default configuration uses `127.0.0.1`, which allows connections from the same machine. For network-wide access, configure an appropriate network interface and firewall permissions.

---

## 💬 Client Commands

| Command | Description |
|---|---|
| `/quit` | Disconnects from the chat room |
| `Ctrl + C` | Interrupts the client application |

When a participant disconnects, the server cleans up the connection and notifies the remaining participants.

---

## 🧠 How It Works

The application follows these steps:

1. **Server Initialization:** Creates a TCP socket and binds it to the configured host and port.
2. **Connection Listening:** Starts listening for incoming client connections.
3. **Client Connection:** Clients establish TCP connections with the server.
4. **Thread Creation:** The server creates a dedicated listener thread for each connected client.
5. **Message Reception:** The server receives messages from connected clients.
6. **Message Broadcasting:** Received messages are distributed to the other active participants.
7. **Timestamp Formatting:** Messages are displayed with the current time.
8. **Disconnection Handling:** Disconnected clients are removed from the active connection list.

### Communication Flow

```text
             TCP CHAT SERVER
                    |
          ---------------------
          |         |         |
       Client 1  Client 2  Client 3
        Alice      Bob      Charlie
          |         |         |
          ---------------------
                    |
             Message Broadcast
```

---

## 📂 Project Structure

```text
chat-application/
│
├── server.py       # Multithreaded TCP chat server
├── client.py       # Interactive TCP chat client
└── README.md       # Project documentation
```

---

## 🛠️ Troubleshooting

| Problem | Possible Cause | Recommended Solution |
|---|---|---|
| Address already in use | Port 5000 is occupied | Start the server on another port |
| Connection refused | Server is not running | Start the server before connecting clients |
| Connection timeout | Incorrect host or network configuration | Verify server IP and network connectivity |
| Client disconnects unexpectedly | Network interruption | Reconnect to the server |
| Python not recognized | Python is missing from PATH | Add Python to PATH or use `py` / `python3` |

### Alternative Port Configuration

If port `5000` is already occupied:

```bash
python server.py --port 5050
```

Connect clients using the same port:

```bash
python client.py --port 5050 -u Alice
```

---

## 🔐 Security Considerations

- The current implementation uses TCP communication without application-level encryption.
- Avoid transmitting passwords or sensitive information.
- Restrict network exposure to trusted environments.
- For production deployment, consider TLS encryption, authentication, input validation, and connection limits.

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome!

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. Commit your changes:

   ```bash
   git commit -m "feat: improve chat functionality"
   ```

4. Push your branch:

   ```bash
   git push origin feature/AmazingFeature
   ```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software in accordance with the license conditions.

---

**Built with Python 🐍**
