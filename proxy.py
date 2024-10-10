"""
******************************************************************************
Author      = Yash Mittal (112101054), Rachit Jain (112101019),

Project     = HTTP Proxy Server

Description = A multithreaded HTTP proxy server that handles both regular HTTP 
              requests and HTTPS CONNECT tunneling. The proxy server listens 
              for incoming client requests, modifies them as needed, forwards 
              them to the destination server, and relays the response back to 
              the client.

Usage       = To run the proxy server, use the following command:
              $ python3 filename [PORT]

              - [PORT] is optional. If not specified, the default port 1234 
                will be used.

              Example:
              $ python3 proxy_server.py      (runs on port 1234)
              $ python3 proxy_server.py 8080 (runs on port 8080)
******************************************************************************
"""

import socket
import threading
import select
import datetime
import sys

BUFFER_SIZE = 4096
PROXY_HOST = '127.0.0.1'

# Helper function to get the current timestamp in "day month hour:minute:second" format.
def get_current_timestamp():
    return datetime.datetime.now().strftime("%d %b %H:%M:%S")

# Extracts the host and port from a CONNECT HTTP request line.
# Defaults to 443 for HTTPS if no port is specified.
def get_connect_host_and_port(request_line):
    parts = request_line.split()
    if len(parts) < 2:
        return None, None
    host_port = parts[1]
    if ':' in host_port:
        host, port = host_port.split(':')
        return host, int(port)
    else:
        return host_port, 443  # Default to port 443 for HTTPS

# Prints the HTTP request line along with a timestamp.
def print_http_request_line(request_line):
    timestamp = get_current_timestamp()
    parts = request_line.split()
    if len(parts) > 1:
        method = parts[0]
        uri = parts[1]
        if method != 'POST':
            print(f"{timestamp} - >>> {method} {uri}")

# Handles CONNECT tunneling requests for HTTPS connections.
# Sets up a tunnel between the client and the remote server and forwards data between them.
def handle_connect_tunneling(client_socket, host, port):
    try:
        # Connect to the target server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))
        client_socket.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")

        # Forward data between client and server
        sockets = [client_socket, remote_socket]
        while True:
            readable, _, _ = select.select(sockets, [], [])
            for sock in readable:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    client_socket.close()
                    remote_socket.close()
                    return
                if sock is client_socket:
                    remote_socket.sendall(data)
                else:
                    client_socket.sendall(data)
    except Exception as e:
        print(f"Error in CONNECT tunneling: {e}")
        client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        client_socket.close()

# Handles a client connection, processes the request, and dispatches the request
# to appropriate handlers based on the HTTP method (e.g., CONNECT or regular HTTP request).
def handle_client(client_socket):
    try:
        request = b""
        while True:
            part = client_socket.recv(BUFFER_SIZE)
            request += part
            if b'\r\n\r\n' in request or b'\n\n' in request:
                break
        
        # Extract headers from the request
        header_end_pos = request.find(b'\r\n\r\n') if b'\r\n\r\n' in request else request.find(b'\n\n')
        headers = request[:header_end_pos].decode('utf-8').splitlines()

        # Get the first request line
        request_line = headers[0]
        print_http_request_line(request_line)

        if request_line.startswith('POST'):
            client_socket.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            client_socket.close()
            return

        # Handle CONNECT tunneling (HTTPS)
        if request_line.startswith('CONNECT'):
            host, port = get_connect_host_and_port(request_line)
            if host and port:
                print_http_request_line(f"CONNECT {host}:{port} HTTP/1.1")
                handle_connect_tunneling(client_socket, host, port)
            else:
                client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                client_socket.close()
        else:
            # Handle regular HTTP requests
            handle_regular_http_request(client_socket, headers, request[header_end_pos+4:])

    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.close()

# Handles regular HTTP requests (non-CONNECT).
# Modifies the request to remove the full URL and adjusts headers for the proxy.
# Then, forwards the request to the destination server and relays the response back to the client.
def handle_regular_http_request(client_socket, headers, body):
    try:
        # Extract Host header to determine the destination server
        host_header = next((header for header in headers if header.lower().startswith('host:')), None)
        if not host_header:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
            return

        # Extract host and port from the Host header
        host_port = host_header.split(":")[1].strip()
        if ':' in host_port:
            host, port = host_port.split(':')
            port = int(port)
        else:
            host = host_port
            port = 80  # Default to port 80 for HTTP

        # Modify the request line to include only the path, not the full URL
        request_line = headers[0]
        parts = request_line.split()
        if len(parts) >= 3:
            method = parts[0]
            url = parts[1]
            if url.startswith('http://'):
                # Find the start of the path after 'http://'
                path_start = url.find('/', 7)
                if path_start != -1:
                    url = url[path_start:]
                else:
                    url = '/' # Default to '/' if no path

            # Modify the request line to downgrade to HTTP/1.0 and keep only the path
            headers[0] = f"{method} {url} HTTP/1.0"

        # Replace 'keep-alive' with 'close' in headers to prevent persistent connections
        headers = [header if 'keep-alive' not in header.lower() else header.replace('keep-alive', 'close') for header in headers]

        # Connect to the destination server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))

        # Forward the modified request to the remote server
        remote_socket.sendall(b'\r\n'.join(line.encode('utf-8') for line in headers) + b'\r\n\r\n' + body)

        # Forward the response from the server back to the client
        while True:
            response = remote_socket.recv(BUFFER_SIZE)
            if len(response) == 0:
                break
            client_socket.sendall(response)

        remote_socket.close()
        client_socket.close()

    except Exception as e:
        print(f"Error in regular HTTP request handling: {e}")
        client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        client_socket.close()

# Starts the proxy server and listens for incoming connections.
def start_proxy(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((PROXY_HOST, port))
    server_socket.listen(5)
    print(f"{get_current_timestamp()} - Proxy listening on {PROXY_HOST}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    # Get the port from the command-line arguments, default to 1234 if not provided
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 1234
    start_proxy(port)
