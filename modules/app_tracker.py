import pyshark.packet.packet as pypacket
import modules.connection as conn
import modules.web_tracker as web_tracker

class App_Tracker:

    def __init__(self, wbtrkr: web_tracker.Web_Tracker):

        self.connections = [] # Living connections
        self.dead_connections = [] # Dead connections
        self.wbtrkr = wbtrkr # The web tracker module
        self.conn_num = 1 # The current connection number we are on

        return

    def accept_packet(self, packet: pypacket.Packet) -> None:

        is_existing = False

        # Check if it is part of a connection
        for connection in self.connections: # NOTE this will consider any communication from a server, even that which is not UDP, as continuing a connection
            if connection.is_ours(packet):

                # If it is, see if we need to make a new connection
                if connection.is_new_connection(packet):

                    # Kill the existing connection
                    self.dead_connections.append(connection)
                    self.connections.remove(connection)

                    # Make a new connection
                    new_conn = conn.Connection(f"Application Connection {self.conn_num}", packet.ip.dst, [packet.ip.src], float(packet.sniff_timestamp))
                    self.connections.append(new_conn)
                    self.conn_num += 1

                else: # If it isn't, accept the packet and return
                    connection.accept_packet(packet)
                    is_existing = True

                return # A packet is only part of one ip
        
        # Check if it is udp for a new connection
        if ("UDP" in packet and "DNS" not in packet and "SSDP" not in packet and "NBNS" not in packet 
            and "DHCP" not in packet and "SMB" not in packet and "MDNS" not in packet and "NTP" not in packet 
            and "DHCPV6" not in packet and "LMNR" not in packet and "QUIC" not in packet and "ICMPV6" not in packet 
            and "ICMP" not in packet and "STUN" not in packet and packet.udp.port != "443"):

            # If it is, grab server ip and check if there is web connection for this
            server_ip = packet.ip.src
            web_conn = self.wbtrkr.has_connection_for(server_ip)

            # If there is setup this connection as complementary to a web connection
            if web_conn:
                new_conn = conn.Connection(web_conn.names[0] + " application traffic", web_conn.user_ip, web_conn.server_ips, web_conn.start_time)
                new_conn.accept_packet(packet)
                self.connections.append(new_conn)
            else: # Otherwise just make a new connection
                # Make a new connection
                new_conn = conn.Connection(f"Application Connection {self.conn_num}", packet.ip.dst, [packet.ip.src], float(packet.sniff_timestamp))
                self.connections.append(new_conn)

            # Increase conn_num
            self.conn_num += 1

        # Return out of void
        return

    def __str__(self) -> str:

        output = "App Tracker Module:<br />"

        for connection in self.connections:
            output += str(connection) + "<br />"

        output += "Dead Connections:<br />"

        for connection in self.dead_connections:
            output += str(connection) + "<br />"
        
        return output