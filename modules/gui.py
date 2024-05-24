import os

USER_FOLDER = "./userFolder"

class GUI:
    def __init__(self, modules: list, fp: str):

        # Init variables
        self.modules = modules
        self.fp = fp

        return
    
    def updateGUI(self) -> None:

        out = open(self.fp, "w")

        # Get all connections
        all_connections = []
        for module in self.modules:
            for connection in module.connections:
                all_connections.append(connection)
            for connection in module.dead_connections:
                all_connections.append(connection)

        # Sort connections by user_ip
        users = {}

        for connection in all_connections:

            uip = connection.user_ip

            if not uip in users:
                users[uip] = []

            users[uip].append(connection)

        # Set up of main page
        out.write("<!DOCTYPE html><head><title>HomeShark</title><style>body{background-color: #e1e1e1;}.scrolls {overflow-x: scroll;overflow-y: hidden;white-space: nowrap;display:flex}.userDiv{box-shadow: 1px 1px 10px #999;margin: 2px;max-height: 550px;height: 550;max-width: 450px;width: 450;overflow-y: scroll;cursor: pointer;display: inline-block;vertical-align: top;padding: 10px 1px 1px 15px;}.connectionDiv{box-shadow: 1px 1px 10px #999;margin: 10px;max-height: 100%;height:fit-content;width:90%;cursor: pointer;vertical-align: middle;padding: 1px 5px 5px 15px;background-color: #e1e1e1;overflow-x: scroll;-ms-overflow-style: none;scrollbar-width: none;}.tb {font-size: 12px;}h1{font-family: Impact, fantasy;}</style></head><html><body><h1> Home Shark </h1><button style='display: inline-flex; align-items: center; justify-content: center; padding: 10px 20px; font-size: 16px; font-family:'Times New Roman', Times, serif; border: none; border-radius: 5px; background-color: #0074D9; color: #ffffff; cursor: pointer; transition: background-color 0.3s ease;\" onclick=\"window.location.reload();\">Refresh</button><hr /><div class='scrolls'><div>") 

        
        # Generate each page by user ip
        for uip in users:

            user_entry = f"<div class='userDiv' ><h2>Connections for User: {uip}</h2>"

            # Get the connection list for this user
            conn_list = users[uip]

            # For each connection
            for conn in conn_list:

                # write each connection
                user_entry += str(conn)

            # End the user entry
            user_entry += "</div>"

            # Write to output
            out.write(user_entry)

        # Finish the page
        out.write("</div></div></body></html>")
        out.close()
        return


# <script>setTimeout(() => {document.location.reload();}, 3000);</script>


if __name__ == "__main__":

    g = GUI([], "")