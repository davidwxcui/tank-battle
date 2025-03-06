import socket
import threading
import random
import os
import TCP_helper

# List to store connected clients
connected_clients = []


def TCP_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Host and port number: {host}:{port}")

        # Start the communicate with client thread
        communication_thread = threading.Thread(target=Server_Message_Sender)
        communication_thread.start()

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=Server_Listener, args=(conn, addr))
            client_thread.start()

def Server_Listener(conn, addr):
    """Function to listen to message from clients, each listener thread is created for each client."""
    print(f"Connected by {addr}")
    connected_clients.append((conn, addr))  # Add the client to the list of connected clients
    with conn:
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    TCP_helper.listener_process(data)
        finally:
            connected_clients.remove((conn, addr))  # Remove the client from the list when disconnected
            conn.close()
            print(f"connection closed successfully{addr}")

def Server_Message_Sender():
    """Function to send message to individual clients."""
    while True:
        if not connected_clients:
            continue

        server_input = input("Enter the client number to communicate with (-1 to exit):Example: 0:Hello World\n")

        if server_input == "-1":
            os._exit(0)

        try:
            client_index, message = server_input.split(":", 1)
            client_index = int(client_index)
        except ValueError:
            print("Invalid input format. Please use the format 'client_number:message'.")
            continue

        if client_index < 0 or client_index >= len(connected_clients):
            print("Invalid client number.")
            print("Connected clients:")
            for i, (client_conn, client_addr) in enumerate(connected_clients):
                print(f"{i}: {client_addr}")
            continue

        client_conn, client_addr = connected_clients[client_index]
        sender_ip = socket.gethostbyname(socket.gethostname())
        sender_name = "Server"

        header = f"{sender_ip}|{sender_name}|"
        full_message = header + message
        encoded_message = full_message.encode()
        checksum = TCP_helper.calculate_checksum(encoded_message)
        encoded_message_with_checksum = encoded_message + checksum.to_bytes(2, 'big')
        client_conn.sendall(encoded_message_with_checksum)

def Client_receive_messages(conn):
    """Function to receive messages from the server."""
    while True:
        data = conn.recv(1024)
        # print(data)
        if data:
            # Validate the checksum
            if not TCP_helper.validate_checksum(data):
                # print(f"Checksum mismatch from {addr}. Dropping packet.")
                continue
            # Decode the message and extract the header
            content = data[:-2].decode()
            message = content.split('|', 2)[:3]

            print(f"Message from server: {message[2]}")
            print("Enter message: ")

def TCP_client(host='127.0.0.1', port=65432):
    input_string = False
    while input_string == False:    
        sender_name = input("Enter your name: ")  # Prompt for sender name
        input_string = TCP_helper.validate_input(sender_name)
    sequence_code = 0
    sender_ip = socket.gethostbyname(socket.gethostname())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, int(port)))
        print("Connected to the server. Type 'exit' to quit.")

        # Start the receive messages thread
        receive_thread = threading.Thread(target=Client_receive_messages, args=(s,))
        receive_thread.start()
    
        while True:
            message = input("Enter message: \n")
            if TCP_helper.validate_input(message) == False:
                print("No message can have use special charactor |.")
                continue
            if message.lower() == 'exit':
                print("Closing connection.")
                break

            # Add header to the message
            full_message = f"{sender_ip}|{sender_name}|{message}"
            encoded_message = full_message.encode()
            checksum = TCP_helper.calculate_checksum(encoded_message)
            encoded_message_withchecksum = encoded_message + checksum.to_bytes(2, 'big')

            # Send the message
            s.sendall(encoded_message_withchecksum)

if __name__ == "__main__":
    role = input("Enter 'server' to start the server or 'client' to start the client: ").strip().lower()
    if role == 'server':
        TCP_server()
    elif role == 'client':
        TCP_client()
    else:
        print("Invalid input. Please enter 'server' or 'client'.")