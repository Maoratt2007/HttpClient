from socket import socket
from struct import pack

NEW_FILE = "/tmp/test.txt"

BUFSIZE = 1024

FORMAT = "!I"

ACTION = "wb"

PORT = 8200

IP = "127.0.0.1"

class ClientHttp:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port

    def connect_socket(self) -> socket:
        """Connect the socket to our client and return this socket"""
        client_socket = socket()
        client_socket.connect((self.ip, self.port))
        print(f"Connecting to {self.ip}:{self.port}")
        return client_socket

    def download_file(self,content_file: bytes, new_file: str):
        """Copy the content of the file to new file->download"""
        with open(new_file, ACTION) as file:
            file.write(content_file)

    def handle_file(self,client_socket):
        """Send to server file_name and then using download_file copy the content of the file to new one"""
        file_name = input("Which file would you like to download? ")
        client_socket.send(file_name.encode())
        content_file = client_socket.recv(BUFSIZE)
        self.download_file(content_file, NEW_FILE)
        print(f"Download file from the server to {NEW_FILE} succeed!")

    def ask_server(self,client_socket, user_choice):
        """ask for server how is he-> state 2"""
        client_socket.send(pack(FORMAT, int(user_choice)))
        print("Asking the server how is he")
        recv_data = client_socket.recv(BUFSIZE).decode()
        print(f"The server answered: {recv_data}")

    def handle_cases(self,client_socket):
        """handle with the 3 cases 1-exit 2-download file 3-how is the server"""
        user_choice = int(
            input("What the action do you ask from the server 1.break 2.download file 3.how is the server: "))
        while user_choice != 1:
            client_socket.send(pack(FORMAT, user_choice))
            ack = client_socket.recv(BUFSIZE).decode()

            if ack != "ACK!":
                print("The server didn't get your choice!")
                break

            if user_choice == 2:
                self.handle_file(client_socket)

            elif user_choice == 3:
                self.ask_server(client_socket, user_choice)

            user_choice = int(
                input("What the action do you ask from the server 1.break 2.download file 3.how is the server: "))

        client_socket.send(pack(FORMAT, int(user_choice)))
        print("Ended communication!")

    def manage_socket(self):
        """manage the socket open and close-> the main function of the system"""
        client_socket = self.connect_socket()
        self.handle_cases(client_socket)
        client_socket.close()



def main():
    http_client=ClientHttp(IP,PORT)
    http_client.manage_socket()

if __name__=="__main__":
    main()