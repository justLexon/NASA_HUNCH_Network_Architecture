import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Initialize colors for console output
init()

colors = [
    Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE,
    Fore.YELLOW
]

client_color = random.choice(colors)  # Randomly choose a color for client
messages


# Server's IP address and port
SERVER_HOST = "192.168.1.140"
SERVER_PORT = 5002

separator_token = "<SEP>"  # Separator token for message formatting


# Initialize TCP socket for client-server communication
s = socket.socket()


# Connect to the server
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except socket.error as e:
    print(f"[!] Error: {e}")
    exit()

print("[+] Connected.")


# Function to listen for messages from the server
def listen_for_messages():
    while True:
        try:
            message = s.recv(1024).decode()  # Receive and decode the message from the server
        except Exception as e:
            print(f"[!] Error: {e}")
            break

        print("\n" + message)  # Print the received message


# Start a thread to listen for messages from the server
t = Thread(target=listen_for_messages)
t.daemon = True  # Make the thread a daemon so it ends when the main thread ends
t.start()


# Prompt for password to connect to the server
password = input("Enter the password to connect to the server: ")

s.send(password.encode())  # Send the password to the server for authentication


# Prompt for user's name
name = input("Enter your name: ")


# Function to send a message to the server
def send_message(message):
    # Format the message with timestamp, user's name, and color
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    formatted_message = f"{client_color}[{date_now}]\n{name}{separator_token}{message}{Fore.RESET}"

    # Send the formatted message to the server
    s.send(formatted_message.encode())


while True:
    try:
        # Get user input for the message to send
        to_send = input()
    except KeyboardInterrupt:
        # Handle Ctrl+C to gracefully exit the program
        print("\n[+] Exiting...")
        send_message("left the chat")  # Notify the server that the user left the chat
        break

    if to_send.lower() == 'q':
        # If user enters 'q', exit the program
        print("\n[+] Exiting...")
        send_message("left the chat")  # Notify the server that the user left the chat
        break

    elif to_send.startswith("/private"):
        # If the message starts with '/private', it's a private message
        recipient_name, message = to_send.split(maxsplit=1)[1].split(maxsplit=1)

        # Extract recipient's name and message
        send_message(f"(Private) {name} -> {recipient_name}: {message}")  # Send the private message to the server

    else:
        # Otherwise, it's a regular message
        send_message(to_send)  # Send the message to the server


# Close the socket
s.close()
