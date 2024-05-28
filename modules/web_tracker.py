import pyshark.packet.packet as pypacket
import modules.connection as conn
from modules.utils import get_dst, get_src

class Web_Tracker:

    def __init__(self):

        self.connections = []
        self.dead_connections = []

        return

    def accept_packet(self, packet: pypacket.Packet) -> None:

        # Check if it is part of a connection
        for connection in self.connections: # TODO killing connections decreases the number we need to check

            if connection.is_ours(packet):
                connection.accept_packet(packet)
                return # A packet is only part of one ip
        
        # Check if it is dns for a new connection
        if "DNS" in packet and "resp_type" in packet.dns.field_names and (packet.dns.resp_type == "1" or packet.dns.resp_type == "5") and hasattr(packet.dns, "a"):

            # get all ips
            all_ips = []
            for field in packet.dns.a.all_fields:
                all_ips.append(field.get_default_value())

            # Is this a new ip for an existing connection (based on domain name)
            for connection in self.connections:
                if packet.dns.qry_name in connection.names: # TODO: Probably faster to save variables than repeatedly do packet.dns.qry_name because they are doing weird stuff
                    connection.expand_server_ips(all_ips)

            # Is this a new ip for an existing connection (based on ip overlap)
            for ip in all_ips: # TODO: really slow probably
                for connection in self.connections:
                    if ip in connection.server_ips:

                        # Check if this is a new connection
                        if not connection.is_new_connection(packet):

                            # If not, expand connection
                            connection.expand_server_ips(all_ips)

                            # and expand names
                            connection.expand_name(packet.dns.qry_name)

                        else: # If we need a new connection

                            # Add connection to dead list
                            self.dead_connections.append(connection)

                            # Remove connection from live list
                            self.connections.remove(connection)

                            # Make a new connection
                            new_connection = conn.Connection(packet.dns.qry_name, get_dst(packet), all_ips, float(packet.sniff_timestamp))
                            self.connections.append(new_connection)

                        return # connections cannot be merged

            # Else make a new connection
            new_connection = conn.Connection(packet.dns.qry_name, get_dst(packet), all_ips, float(packet.sniff_timestamp))
            self.connections.append(new_connection)

        # Return out of void
        return

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

                print("killed a connection")

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