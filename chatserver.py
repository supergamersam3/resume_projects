import threading
import socket

host = '127.0.0.1' # localhost
port = 45555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

clients = []

usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} left the chat!'.encode('ascii'))
            usernames.remove(username)
            break

def recive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.appenda(username)
        clients.append(client)

        print(f'nickname of the client is {username}!')
        broadcast(f'{username} joined chat!'.encode('ascii'))
        client.send('connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server is up ...")
recive()