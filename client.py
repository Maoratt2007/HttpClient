from socket import socket
from struct import pack

BUFSIZE = 1024

FORMAT = "!I"

ACTION = "wb"

PORT = 8200

IP = "127.0.0.1"


def connect_socket()->socket:
    """Connect the socket to our client and return this socket"""
    client_socket= socket()
    client_socket.connect((IP, PORT))
    print(f"Connecting to {IP}:{PORT}")
    return client_socket

def download_file(content_file: bytes, new_file:str):
    """Copy the content of the file to new file->download"""
    with open(new_file, ACTION) as file:
        file.write(content_file)

def handle_file(client_socket):
    """Send to server file_name and then using download_file copy the content of the file to new one"""
    file_name = input("Which file would you like to download? ")
    client_socket.send(file_name.encode())
    content_file = client_socket.recv(BUFSIZE)
    download_file(content_file, file_name)
    print(f"Download file from the server to {file_name} succeed!")

def ask_server(client_socket, user_choice):
    """ask for server how is he-> state 2"""
    client_socket.send(pack(FORMAT, int(user_choice)))
    print("Asking the server how is he")
    recv_data = client_socket.recv(BUFSIZE).decode()
    print(f"The server answered: {recv_data}")

def handle_cases(client_socket):
    """handle with the 3 cases 1-exit 2-download file 3-how is the server"""
    user_choice = input("What the action do you ask from the server 1.break 2.download file 3.how is the server: ")
    while user_choice != 1:
        if user_choice == 2:
            handle_file(client_socket)

        elif user_choice == 3:
            ask_server(client_socket, user_choice)

        user_choice = input("What the action do you ask from the server 1.break 2.download file 3.how is the server: ")

    client_socket.send(pack(FORMAT, int(user_choice)))
    print("Ended communication!")



def main():
    client_socket=connect_socket()
    handle_cases(client_socket)
    client_socket.close()

if __name__=="__main__":
    main()