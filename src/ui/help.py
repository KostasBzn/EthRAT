from src.ui.colors import Colors as cl

def help():
    """ Help Menu """
    print(cl.green + """
    |---------------------------------|--------------------------------------------|
    |      Commands                   |                Description                 |
    |---------------------------------|--------------------------------------------|
    |---------------------------------|----Main Menu-------------------------------|
    |       help                      | Display help menu                          |
    |       list                      | List the connected clients                 |
    |       0                         | Broadcast to all clients                   |
    |       <clientId>                | Interract with client                      |
    |       exit                      | Stop the server                            |
    |---------------------------------|--Interracting mode-------------------------|
    |       kill                      | Kill connection with client                |
    |       download <file/folder>    | Download file/directory from client        |
    |       upload                    | Upload file to client (opens file dialog)  |
    |       cd                        | Browse to a directory                      |
    |       getip                     | Get the clients public and local IP        |
    |---------------------------------|--------------------------------------------|
    """ + cl.reset)