def validate_input(input_string):
    """Validate that the input string does not contain the forbidden character '|'."""
    if '|' in input_string:
        print("Error: '|' character is not allowed in the input.")
        return False
    return True

def calculate_checksum(message):
    """Calculate a 4-digit checksum for the given message."""
    checksum = sum(message) % 10000
    return checksum

def validate_checksum(message):
    """Validate the checksum of the received message."""
    received_message = message[:-2]
    received_checksum = int.from_bytes(message[-2:], 'big')
    calculated_checksum = calculate_checksum(received_message)
    return calculated_checksum == received_checksum

def listener_process(data):
    """"{sender_ip}|{sender_name}|{message}"""
    # print(f"Received message from {addr}: {data}")
    # Validate the checksum
    if not validate_checksum(data):
        # print(f"Checksum mismatch from {addr}. Dropping packet.")
        return False
    # Decode the message and extract the header
    content = data[:-2].decode()
    message = content.split('|', 2)[:3]
    print(f"Received message from {message[1]}: {message[2]}")
    return True

