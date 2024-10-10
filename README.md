```markdown
# HTTP Proxy Server

A multithreaded HTTP proxy server designed to handle both regular HTTP requests and HTTPS CONNECT tunneling. This server acts as an intermediary, forwarding client requests to destination servers, modifying them as needed, and relaying responses back to the client.

## Features

- **Multithreaded**: Supports multiple clients simultaneously using threading.
- **HTTPS Support**: Handles HTTPS CONNECT requests by setting up secure tunnels between clients and servers.
- **Regular HTTP Requests**: Forwards and processes regular HTTP requests, modifying them when needed (e.g., removing full URLs).
- **Error Handling**: Properly handles errors like unsupported HTTP methods and bad gateway responses.

## Getting Started

### Prerequisites

- Python 3.x
- Socket and threading libraries (included with Python's standard library)

### Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```

### Usage

To start the proxy server, run the following command:
```bash
python3 proxy_server.py [PORT]
```

- `[PORT]` is optional. If not specified, the default port `1234` will be used.

#### Example:

```bash
python3 proxy_server.py      # runs on port 1234
python3 proxy_server.py 8080 # runs on port 8080
```

### Functionality

- The proxy server listens for incoming client connections.
- It supports both **regular HTTP** and **HTTPS CONNECT tunneling** requests.
- For regular HTTP requests, the proxy modifies the request to remove the full URL and adjusts headers as necessary.
- For HTTPS, it creates a tunnel between the client and the remote server to forward data.

### Logs

- The server logs each request method and the URI along with a timestamp (except for POST requests).
- For CONNECT requests, it logs the host and port information.

## Authors
Here is the `README.md` in markdown format:

```markdown
# HTTP Proxy Server

A multithreaded HTTP proxy server designed to handle both regular HTTP requests and HTTPS CONNECT tunneling. This server acts as an intermediary, forwarding client requests to destination servers, modifying them as needed, and relaying responses back to the client.

## Features

- **Multithreaded**: Supports multiple clients simultaneously using threading.
- **HTTPS Support**: Handles HTTPS CONNECT requests by setting up secure tunnels between clients and servers.
- **Regular HTTP Requests**: Forwards and processes regular HTTP requests, modifying them when needed (e.g., removing full URLs).
- **Error Handling**: Properly handles errors like unsupported HTTP methods and bad gateway responses.

## Getting Started

### Prerequisites

- Python 3.x
- Socket and threading libraries (included with Python's standard library)

### Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```

### Usage

To start the proxy server, run the following command:
```bash
python3 proxy_server.py [PORT]
```

- `[PORT]` is optional. If not specified, the default port `1234` will be used.

#### Example:

```bash
python3 proxy_server.py      # runs on port 1234
python3 proxy_server.py 8080 # runs on port 8080
```

### Functionality

- The proxy server listens for incoming client connections.
- It supports both **regular HTTP** and **HTTPS CONNECT tunneling** requests.
- For regular HTTP requests, the proxy modifies the request to remove the full URL and adjusts headers as necessary.
- For HTTPS, it creates a tunnel between the client and the remote server to forward data.

### Logs

- The server logs each request method and the URI along with a timestamp (except for POST requests).
- For CONNECT requests, it logs the host and port information.

## Authors

- Yash Mittal 
- Rachit Jain 
```

