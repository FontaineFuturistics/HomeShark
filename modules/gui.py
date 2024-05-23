class GUI:

    def __init__(self, modules: list, fp: str):

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

        # TODO initial setup
        out.write("<!DOCTYPE html><html><head><title>HomeShark</title><meta charset=\"UTF-8\"><meta http-equiv=\"refresh\" content = \"5; URL=file:///home/kali/Documents/output.html\" /></head>") # Automatically refresh the page

        # Generate each column by user ip
        for uip in users:

            # TODO Setup user

            # Get the connection list for this user
            conn_list = users[uip]

            # For each connection
            for conn in conn_list:

                # TODO: setup connection
                out.write(str(conn))

        # Finish the method
        out.close()
        return