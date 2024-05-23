import os

USER_FOLDER = "./userFolder"

class GUI:
    def __init__(self, modules: list, fp: str):

        # Clear the userFolder
        for filename in os.listdir(USER_FOLDER):
            try:
                os.remove(os.path.join(USER_FOLDER, filename))
                print(f"Deleted outdated user file {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")

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
        out.write(
            "<!DOCTYPE html> " +
                "<head> "
                    "<style>"+
                        ".scrolls {overflow-x: scroll; overflow-y: hidden; white-space:nowrap}"+
                        ".iframeDiv iframe{box-shadow: 1px 1px 10px #999; margin: 2px; max-height: 50px; cursor: pointer; display:inline-block; vertical-align:top}"+
                    "</style>"+
                "</head>"+
                "<h1> This is main page text <h1>"+
                "<div class='scrolls'>"
                ) 

        
        # Generate each page by user ip
        for uip in users:
            
            # TODO Setup user
            newFileLocation = "./userFolder/" + uip + ".html"
            user_out = open(newFileLocation, "w")#Creates dedicated user page in userFolder
            user_out.write("<!DOCTYPE html> <html> <h2> Connections for User: " + uip + "</h2>")

            # Get the connection list for this user
            conn_list = users[uip]

            # For each connection
            for conn in conn_list:

                # TODO: setup connection
                user_out.write(str(conn))
            
            user_out.write("</html>")
            user_out.close()
            #Add this user to the main page
            out.write("<iframe src='" + newFileLocation + "' height=550></iframe>")

        # Finish the page
        out.write("</div> </html>")
        out.close()
        return


# <script>setTimeout(() => {document.location.reload();}, 3000);</script>


if __name__ == "__main__":

    g = GUI([], "")