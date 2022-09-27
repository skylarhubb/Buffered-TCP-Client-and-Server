# TODO: add any import statements required
from email.header import Header
from socket import *
from struct import pack, unpack
from buffered_server import HEADER_LENGTH

class BufferedTCPClient:

    def __init__(self, server_host='cirrus4.computing.clemson.edu', server_port=3602, buffer_size=1024):
        self.buffer_size = buffer_size

        # TODO: Create a socket and establish a TCP connection with server 
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)

        self.tcp_client_socket.connect((server_host, server_port))


    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should accept a message
    # from the user, which is packed according to the format specified for this assignment and then sent into the socket.
    # TODO: * Send a message to the server containing the message passed in to the function. 
    #           * Remember to pack it using the format defined in the instructions. 
    def send_message(self, message):
        print("CLIENT: Attempting to send a message...")
        print(message)
        
        data = pack("!I" + str(len(message)) + "s", len(message), message.encode())
        self.tcp_client_socket.send(data)


    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should wait to receive a 
    # message from the socket, which is then returned to the user. It should return two values: the message received and whether or not it was received 
    # successfully. In the event that it was not received successfully, return an empty string for the message.
    # TODO: * Return the *string* sent back by the server. This should be the same string you sent, except that first 10 characters will have been removed
    #           * Be sure to set the bufsize parameter to self.buffer_size when calling the socket's receive function
    #           * Remember that we're sending packed messages back and forth, for the format defined in the assignment instructions. You'll have to unpack
    #             the message and return just the string. Don't return the raw response from the server.
    #       * Handle any errors associated with the server disconnecting
    def receive_message(self):
        print("CLIENT: Attempting to receive a message...")

        first_part = self.tcp_client_socket.recv(HEADER_LENGTH)

        received = True
        buffer = b""

        if(first_part):
            # Stripping out the header
            message_length = unpack("!I", first_part[:4])[0]
            print("New message size: " + str(message_length))
            print("Received '", first_part[4:].decode() + "'")
            
            message = first_part[4:]

            while(len(message)) < message_length:
                second_part = min(self.buffer_size, message_length - len(message))
                first_part = self.tcp_client_socket.recv(second_part)
                message += first_part

            return message.decode(), received

        else:
            received = False 
            return buffer.decode(), received


    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should close your socket.
    # TODO: Close your socket
    def shutdown(self):
        print("Client: Attempting to shut down...")
        self.tcp_client_socket.close()

        
if __name__ == "__main__":
    l = BufferedTCPClient(server_host="localhost", server_port=36001)

    l.send_message("Four score and seven years ago")
    response = l.receive_message()
    print(response)
