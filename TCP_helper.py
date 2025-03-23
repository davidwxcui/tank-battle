import struct
import random
import sys
import os
sys.path.insert(0, os.path.abspath('./tank-war-game/src'))
import game
import threading



def generate_unique_id(ID_list):
    """Function to generate a unique ID that is not in the ID_list."""
    while True:
        id = random.randint(0, 255)
        if id not in ID_list:
            ID_list.append(id)
            return id

def validate_input(input_string):
    """Validate that the input string does not contain the forbidden character '|'."""
    if '|' in input_string:
        print("Error: '|' character is not allowed in the input.")
        return False
    return True

def listener_process(data,conn):
    # data 0 - 9 are reserved for client/client messages
    if data[0]==1:
        id, x, y, direction = struct.unpack('!IhhH', data[1:])
        print(f"Movement message received id{id} x{x} y{y} direction{direction}")

    elif data[0]==2:
        shooter_id, x, y, direction = struct.unpack('!IhhH', data[1:])
        print(f"Shooting message received id{shooter_id} x{x} y{y} direction{direction}")

    elif data[0]==3:
        player_id, opponent_id, x, y = struct.unpack('!IhhH', data[1:])
        print(f"Cannonball hit message received player_id{player_id} opponent_id{opponent_id} x{x} y{y}")

    elif data[0]==4:
        message = data[1:]
        content = message.decode()
        message = content.split('|', 2)[:3]
        print(f"Received message from {message[1]}: {message[2]}")

    elif data[0]==5:
        print("client reveal its position message received")

    elif data[0]==6:
        print("player eliminated message received")

    # data 10 - 19 are reserved for server/client messages
    elif data[0]==11:
        print("init message received from client")
    elif data[0]==12:
        x, y, id = struct.unpack('!iii', data[1:])
        print(f"init message received from server id{id} x{x} y{y}")

    elif data[0]==13:
        print("opponent init message received")
    elif data[0]==14:
        print("opponent movement message received")

    else:
        print("Unknown message type received")
        print(data[0])
        print(data[1:])

def recv_chunks(conn, length):
    data = b''
    while len(data) < length:
        packet = conn.recv(length - len(data))
        if not packet:
            print("No packet")
            return None #no data, connection was closed
        data += packet
    return data
    

# when client connect to server , send a message #11 (initiation message) to request a location./ ID etc
# when server got #11 reply #12(prefix) , return back location/ id
# the server also need to send out #13 to other clients alone with #12 , who is joining / location/ id etc.
# after the other clients get message #13, they have to reveal their locaiton to the initiating client by sending #5

 

