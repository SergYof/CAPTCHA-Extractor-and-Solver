import requests
import os
from urllib import parse
from socketServer.client import create_client_ms


def processPicture(picURL: str) -> bytes | None:

    picURL = parse.unquote(picURL) # decode the URL supplied in a GET request
    response = requests.get(picURL) # download the picture with the given URL
    
    # check for HTTPError
    if response.status_code != 200:
        print(f"An error occured downloading the picture. Response code: {response.status_code}")
        return None

    # make a downloads folder if it's not there
    if not os.path.exists("./downloads"):
        os.mkdir("./downloads")
    
    with create_client_ms() as client: 
        client.send(response.content) # send the binary picture over sockets
        print("Picture sent successfully!")
        print("Awaiting response...")
        solution: bytes = client.receive()
    
    print("Solution received (raw bytes): " + solution.hex())
    return solution
