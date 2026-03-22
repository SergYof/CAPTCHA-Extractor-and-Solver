import requests
import os
from urllib import parse


def processPicture(picURL: str) -> str:
    # TODO: return a list of indices to check.
    # download picture
    
    msg: str
    picURL = parse.unquote(picURL) # decoding the URL supplied in a GET request

    print(f"\n\n{picURL=}\n\n")
    
    response = requests.get(picURL)
    
    # check for HTTPError
    if response.status_code != 200:
        msg = f"An error occured downloading the picture. Response code: {response.status_code}"
        print(msg)
        return msg

    # make a folder if it's not there
    if not os.path.exists("./downloads"):
        os.mkdir("./downloads")
    
    # write the picture into the file
    with open("./downloads/CAPTCHA.jpg", "wb") as picFile:
        picFile.write(response.content)
        msg = "Picture downloaded successfully!"
    
    # TODO: find the indices for squares to tick
    print(msg)

    # TODO: feed the picture into LLM and get the LLM response about what to tick
    
    # TODO: return a JSON-formatted response
    return msg
