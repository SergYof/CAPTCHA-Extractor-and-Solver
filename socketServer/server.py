from socket import socket, timeout, AF_INET, SOCK_STREAM
from protocol import MessageSocket, PORT
from threading import Thread, Lock
from PIL import Image
from io import BytesIO


client_ms: MessageSocket
socket_lock = Lock()    # avoid simultaneous sending of information through a socket


def create_listening_socket() -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("127.0.0.1", PORT))
    sock.listen(1)
    sock.settimeout(2)
    return sock


def accept_client_ms(server_sock: socket) -> MessageSocket:
    client_sock, _ = server_sock.accept()
    return MessageSocket(client_sock)


def cut_picture(image: bytes) -> list[Image.Image]:
    img = Image.open(BytesIO(image))    # this avoids saving image to a file and uses an in-memory buffer
    width, height = img.size
    
    # challenge images are usually 300 by 300 px, so it divides nicely
    cell_w = width // 3
    cell_h = height // 3

    pieces = []

    for row in range(3):
        for col in range(3):
            left = col * cell_w
            upper = row * cell_h
            right = left + cell_w
            lower = upper + cell_h

            cropped = img.crop((left, upper, right, lower))
            pieces.append(cropped)
    
    return pieces


def thread_body(image_stream: bytes) -> None:
    tiles = cut_picture(image_stream) 

    # if this runs, the test has passed
    print(f"The size of the first tile is: {tiles[0].size}")
    tiles[0].show("IT WORKS!")

    # TODO call Object Recognition API
    # with the list of retrieved pictures
    # and ask it to recognize the objects requested

    response = b"Socket Server Thread: the picture was received successfully!"
    with socket_lock:
        client_ms.send(response) # reroute the API response to the Flask server
    
    return


def main() -> None:
    server_sock = create_listening_socket()
    print("Socket Server online")

    listen_printed = False # avoid duplication of listening statement
    try:
        while True:
            try:
                if not listen_printed:
                    listen_printed = True
                    print("Listening")
                
                global client_ms
                client_ms = accept_client_ms(server_sock)
                
                print("Connection established")
                picture_bytes = client_ms.receive()
                print("Data received")
                
                Thread(target=thread_body, args = (picture_bytes,)).run()
                
                listen_printed = False
            except timeout:
                pass    # every 2 seconds (socket timeout), Python checks whether Ctrl+C is pressed
    except KeyboardInterrupt:
        print("Stopped with Ctrl + C")


if __name__ == "__main__":
    main()