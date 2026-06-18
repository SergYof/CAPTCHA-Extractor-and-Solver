from subprocess import Popen, CREATE_NEW_CONSOLE

# starts Flask server and socket server as subprocesses in two dedicated console windows
Popen(
    ["cmd", "/k", ".venv\\Scripts\\python.exe", "run_flask.py"],
    creationflags=CREATE_NEW_CONSOLE
)


Popen(
    ["cmd", "/k", ".venv\\Scripts\\python.exe", "-m", "socketServer.server"],
    creationflags=CREATE_NEW_CONSOLE
)