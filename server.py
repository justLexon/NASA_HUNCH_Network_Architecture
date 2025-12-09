import socket
from threading import Thread
import logging

# Configure logging to log messages to a file
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server's IP address and port
SERVER_HOST = "192.168.1.140"
SERVER_PORT = 5002

separator_token = "<SEP>"  # Separator token for message formatting
PASSWORD = "secret123"     # Password required to connect

# Initialize set to store all connected client sockets
client_sockets = set()

# Create a TCP socket for the server
s = socket.socket()

# Make the port reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the specified address and port
try:
    s.bind((SERVER_HOST, SERVER_PORT))
except socket.error as e:
    print(f"[!] Error: {e}")
    exit()

# Listen for incoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


# Function to handle communication with a client
def handle_client_connection(client_socket):

    # Prompt the client to enter the password
    client_socket.send("Please enter the password: ".encode())
    password_attempt = client_socket.recv(1024).decode().strip()

    # Check if the password is correct
    if password_attempt != PASSWORD:
        print(f"[!] Password incorrect. Connection from {client_socket.getpeername()} rejected.")
        client_socket.send("Password incorrect. Connection rejected.".encode())
        client_socket.close()
        return

    # If the password is correct, notify and accept the connection
    print(f"[+] {client_socket.getpeername()} connected successfully.")
    client_sockets.add(client_socket)

    # Function to listen for messages from the client
    def listen_for_messages(client_socket):
        while True:
            try:
                # Receive a message from the client
                msg = client_socket.recv(1024).decode()
            except Exception as e:
                # Handle client disconnection
                print(f"[!] Error: {e}")
                client_sockets.remove(client_socket)
                break

            else:
                # Replace the separator token with ": " for printing
                msg = msg.replace(separator_token, ": ")

                # Log the message
                logging.info(msg)

                # Print the message to the console
                print(msg)

                # Iterate over all connected sockets and send the message
                for cs in client_sockets:
                    cs.send(msg.encode())

    # Start a thread to listen for messages from the client
    t = Thread(target=listen_for_messages, args=(client_socket,))
    t.daemon = True  # Make the thread a daemon so it ends when the main thread ends
    t.start()


# Main loop to accept incoming connections
while True:
    try:
        # Accept a new connection
        client_socket, client_address = s.accept()
    except socket.error as e:
        # Handle socket errors
        print(f"[!] Error: {e}")
        continue

    # Start a new thread to handle the client connection
    t = Thread(target=handle_client_connection, args=(client_socket,))
    t.daemon = True  # Make the thread a daemon so it ends when the main thread ends
    t.start()


# Close the server socket
s.close()
