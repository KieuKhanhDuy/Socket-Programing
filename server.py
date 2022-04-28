import socket
import sys
import threading
import time
import hash

# IP Address and Port
HOST = '127.0.0.1'  
PORT = 8080 

# Key to ensure integrity msg
SECRET_KEY = "5D2E44719232EA78CD2B32"  

# Create socket 
# Listen max 2 socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)

# Function sent message to client
def sent_msg(client):
    while True:
        msg = input('\nSent to client: ')
        if len(msg) == 0: 
            continue

        time.sleep(0.2)

        # Hash msg and send msg + hash code
        hash_code = hash.get_hash_code(msg, SECRET_KEY)
        data_sent = msg + '|' + hash_code

        # Send data with TCP
        client.sendall(bytes(data_sent, "utf8"))        


# Function receive data to client
def rev_msg(client):
    while True:
        # Receive data
        data = client.recv(1024)
        msg_rev, hash_code_rev = data.decode("utf8").split('|')

        # Check integrity of mesage
        if hash.check_integrity_msg(msg_rev, SECRET_KEY, hash_code_rev):
            print("\nReceive from client: " + msg_rev)
        else:
            print("\nThe received message has lost its integrity")

        time.sleep(0.2)


while True:
    # Accept client connect to server 
    # Create client socket
    client, addr = s.accept()
    
    try:
        print('Connected by', addr)

        # Thread sent message
        th1 = threading.Thread(target=sent_msg, args=(client,))

        # Thread receive data
        th2 = threading.Thread(target=rev_msg, args=(client,))

        # Set two thread is Deamon
        th1.daemon = True
        th2.daemon = True

        # Start thread
        th1.start()
        th2.start()

        time.sleep(1)

        # End thread
        th1.join()
        th2.join()

    finally:
        client.close()

s.close()
