from socket import socket, timeout, AF_INET, SOCK_STREAM
from .protocol import SecureConnection, PORT, Message, MessageType
from threading import Thread
from PIL import Image
from io import BytesIO


client_conn: SecureConnection


def create_listening_socket() -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("127.0.0.1", PORT))
    sock.listen(1)
    sock.settimeout(2)
    return sock


def accept_client_conn(server_sock: socket) -> SecureConnection:
    client_sock, _ = server_sock.accept()
    return SecureConnection(client_sock, True)


def cut_picture(image: bytes) -> list[Image.Image]:
    img = Image.open(BytesIO(image))    # this avoids saving image to a file and uses an in-memory buffer
    width, height = img.size
    print(f"Image size is {img.size}")
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


def thread_body(instruction_text: str, image_stream: bytes) -> None:
    tiles = cut_picture(image_stream)

    # if this runs, the test has passed
    print(f"The instruction text is: {instruction_text}")
    print(f"The size of the first tile is: {tiles[0].size}")
    tiles[0].show()

    # TODO call Object Recognition API
    # with the list of retrieved pictures
    # and the instruction text provided
    # and ask it to recognize the objects requested

    response = "Socket Server Thread: the picture was received successfully!"
    client_conn.send(
        Message(MessageType.TEXT, response)
    ) # reroute the API response to the Flask server


def main() -> None:
    server_sock = create_listening_socket()
    print("Socket Server online")

    listen_printed = False # avoid duplication of listening statement
    try:
        while True:
            try:
                if not listen_printed:
                    print("Listening")
                
                listen_printed = True
                
                
                global client_conn
                client_conn = accept_client_conn(server_sock)
                print("Connection established")

                instruction_text = client_conn.receive().payload
                picture_bytes = client_conn.receive().payload
                print("Data received")
                
                Thread(target=thread_body, args = (instruction_text, picture_bytes)).run()
                
                listen_printed = False
            except timeout:
                pass    # every 2 seconds (socket timeout), Python checks whether Ctrl+C is pressed
    except KeyboardInterrupt:
        print("Stopped with Ctrl + C")


if __name__ == "__main__":
    main()