from pathlib import Path
from time import strftime, localtime
from modules.utils import byte_str

MAIN_PAGE_TEMPLATE = "./html_templates/main.html"
USER_DIV_TEMPLATE = "./html_templates/user_div.html"
STYLE_TAGS = "./html_templates/style_tags.css"

class GUI:
    def __init__(self, modules: list, fp: str):

        # Init variables
        self.modules = modules
        self.fp = fp
        self.time = 0

        # Get templates
        self.main_page = Path(MAIN_PAGE_TEMPLATE).read_text()
        self.user_div = Path(USER_DIV_TEMPLATE).read_text()
        self.style_tags = Path(STYLE_TAGS).read_text()

        return
    
    def updateGUI(self) -> None:

        # Get all connections
        all_connections = []
        dead_connections = []
        for module in self.modules:
            for connection in module.connections:
                all_connections.append(connection)
            for connection in module.dead_connections:
                dead_connections.append(connection)
        for connection in dead_connections:
            all_connections.append(connection)

        # Sort connections by user_ip
        users = {}

        # sort total connection size similarly
        size = {}

        for connection in all_connections:

            uip = connection.user_ip

            if not uip in users:
                users[uip] = []
                size[uip] = 0

            users[uip].append(connection)
            size[uip] += (connection.volume * connection.discard_base)

        # variable for user list
        user_list = ""
        
        # Generate each page by user ip
        for uip in users:

            # variable for the connections for this user
            conn_divs = ""

            # Get the connection list for this user
            conn_list = users[uip]

            # For each connection
            for conn in conn_list:

                # write each connection
                conn_divs += str(conn)

            # Add them to the user list
            user_list += self.user_div.format(user_name=uip, connection_div_list=conn_divs, user_data=byte_str(size[uip]))

        # Finish the page
        new_page = self.main_page.format(styles=self.style_tags, user_div_list=user_list, time=strftime('%H:%M:%S', localtime(self.time)))
        out = open(self.fp, "w")
        out.write(new_page)
        out.close()
        return


# <script>setTimeout(() => {document.location.reload();}, 3000);</script>


if __name__ == "__main__":

    g = GUI([], "")