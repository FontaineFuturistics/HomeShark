import pyshark.packet.packet as pypacket
import modules.connection as conn
from modules.utils import get_dst, get_src

class Web_Tracker:

    def __init__(self):

        self.connections = []
        self.dead_connections = []

        return

    def accept_packet(self, packet: pypacket.Packet) -> bool:

        accepted = False

        # Check if it is part of a connection
        for connection in self.connections: # TODO killing connections decreases the number we need to check

            # Tell the connection to handle it
            if connection.handle_packet(packet):
                accepted = True
                break # If the connection accepted it, stop processing
        else:

            if "DNS" in packet:
                # Else make a new connection
                all_ips = []
                for field in packet.dns.a.all_fields:
                    all_ips.append(field.get_default_value())
                new_connection = conn.Connection(packet.dns.qry_name, get_dst(packet), all_ips, float(packet.sniff_timestamp))
                self.connections.append(new_connection)
                accepted = True

        # Return out of void
        return accepted

    # Checks if a connection exists for an ip, if so returns the connection, if not returns None
    def has_connection_for(self, server_ip: str) -> conn.Connection:

        for connection in self.connections:
            if server_ip in connection.server_ips:
                return connection
        for connection in self.dead_connections:
            if server_ip in connection.server_ips:
                return connection
        return None
    
    def find_dead_connections(self, current_time: float) -> None:

        for connection in self.connections:

            if connection.is_dead(current_time):

                connection.is_alive = False                
                self.dead_connections.append(connection)
                self.connections.remove(connection)
    
    def __str__(self) -> str:

        output = "Web Tracker Module:<br />"

        for connection in self.connections:
            output += str(connection) + "<br />"

        output += "Dead Connections:<br />"

        for connection in self.dead_connections:
            output += str(connection) + "<br />"
        
        return output