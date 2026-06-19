import requests
from urllib import parse
from socketServer import create_client_conn
from socketServer.protocol import Message, MessageType


def processPicture(arguments: dict[str, str]) -> dict[str, str | None]:
    """
    Processes a sent picture and instruction text, sending it over to the socket server.
    Returns a dictionary of socket server's response or error.
    """

    instructionText = arguments.get("instructionText")
    picURL = arguments.get("picURL")
    
    if not(instructionText and picURL):
        return {"response": None, "error": "Malformed API request"}

    picURL = parse.unquote(picURL) # decode the URL supplied in a GET request
    response = requests.get(picURL) # download the picture with the given URL
    
    # check for HTTPError
    if response.status_code != 200:
        print(f"An error occured downloading the picture. Response code: {response.status_code}")
        return {"response": None, "error": "Error downloading the picture"}

    
    with create_client_conn() as client: 
        # send the instruction text and binary picture over sockets
        client.send(Message(MessageType.TEXT, instructionText))
        client.send(Message(MessageType.BINARY, response.content))
        print("Picture sent successfully!")

        print("Awaiting response...")
        solution = client.receive().payload
    
    print("Solution received: " + solution)
    return {"response": solution, "error": None}
