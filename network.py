import socket
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_PASSWORD = os.getenv("GAME_PASSWORD", "defaultpass")

def host_game(port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    print(f"Hosting game on port {port}. Waiting for friend...")
    
    conn, addr = server.accept()
    
    # Authenticate Guest
    client_hash = conn.recv(1024).decode()
    expected_hash = hashlib.sha256(SECRET_PASSWORD.encode()).hexdigest()
    
    if client_hash != expected_hash:
        print("Unauthorized connection attempt blocked.")
        conn.send("DENIED".encode())
        conn.close()
        return None
        
    conn.send("ACCEPTED".encode())
    print(f"Friend connected securely from {addr}!")
    return conn

def join_game(host_ip, port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host_ip, port))
        # Send password hash
        password_hash = hashlib.sha256(SECRET_PASSWORD.encode()).hexdigest()
        client.send(password_hash.encode())
        
        response = client.recv(1024).decode()
        if response == "ACCEPTED":
            print("Successfully securely connected to host!")
            return client
        else:
            print("Connection denied. Check your password.")
            return None
    except Exception as e:
        print(f"Could not connect: {e}")
        return None