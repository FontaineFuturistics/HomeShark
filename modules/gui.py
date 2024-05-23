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
        out.write("<!DOCTYPE html><head><title>HomeShark</title><style>.scrolls {overflow-x: scroll;overflow-y: hidden;white-space: nowrap;display:flex}.iframeDiv, iframe {box-shadow: 1px 1px 10px #999;margin: 2px;max-height: 700px;height: 700;max-width: 450px;overflow-y: scroll;cursor: pointer;display: inline-block;vertical-align: top;padding: 10px 0px 0px 10px;}.tb {font-size: 12px;}</style></head><html><body><h1> This is main page text </h1><button style=\"display: inline-flex; align-items: center; justify-content: center; padding: 10px 20px; font-size: 16px; border: none; border-radius: 5px; background-color: #0074D9; color: #ffffff; cursor: pointer; transition: background-color 0.3s ease;\" onclick=\"window.location.reload();\">Refresh Page</button><div class='scrolls'>") 

        
        # Generate each page by user ip
        for uip in users:

            user_entry = f"<div class='iframeDiv' ><h2>Connections for<br />User: {uip}</h2><p class=\"tb\">"

            # Get the connection list for this user
            conn_list = users[uip]

            # For each connection
            for conn in conn_list:

                # write each connection
                user_entry += str(conn)

            # End the user entry
            user_entry += "</p></div>"

            # Write to output
            out.write(user_entry)

        # Finish the page
        out.write("</div></body></html>")
        out.close()
        return


# <script>setTimeout(() => {document.location.reload();}, 3000);</script>


if __name__ == "__main__":

    g = GUI([], "")