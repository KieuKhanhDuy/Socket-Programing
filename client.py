import socket
import threading
import time
import hash

# IP Address and Port
HOST = '127.0.0.1'  
PORT = 8080      

# Key to ensure integrity msg
SECRET_KEY = "5D2E44719232EA78CD2B32"  

# Create socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to %s port ' %str(server_address))
s.connect(server_address)

# Function sent message to server
def sent_msg():
    while True:
        msg = input('\nSent to server: ')
        if len(msg) == 0: 
            continue

        time.sleep(0.2)

        # Hash msg and send msg + hash code
        hash_code = hash.get_hash_code(msg, SECRET_KEY)
        data_sent = msg + '|' + hash_code

        # Send data with TCP
        s.sendall(bytes(data_sent, "utf8"))

# Function receive data to server
def rev_msg():
    while True:
        # Receive data
        data = s.recv(1024)
        msg_rev, hash_code_rev = data.decode("utf8").split('|')

        # Check integrity of mesage
        if hash.check_integrity_msg(msg_rev, SECRET_KEY, hash_code_rev):
            print('\nReceive from server: ', msg_rev)    
        else:
            print("\nThe received message has lost its integrity")

        time.sleep(0.2)


try:
    # Thread sent message
    th1 = threading.Thread(target=sent_msg, name='t1')

    # Thread receive data
    th2 = threading.Thread(target=rev_msg, name='t2')

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
    s.close()