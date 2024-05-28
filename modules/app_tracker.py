import pyshark.packet.packet as pypacket
import modules.connection as conn
import modules.web_tracker as web_tracker
from modules.utils import get_dst, get_src

class App_Tracker:

    def __init__(self, wbtrkr: web_tracker.Web_Tracker):

        self.connections = [] # Living connections
        self.dead_connections = [] # Dead connections
        self.wbtrkr = wbtrkr # The web tracker module
        self.conn_num = 1 # The current connection number we are on

        return

    def accept_packet(self, packet: pypacket.Packet) -> bool:

        accepted = False

        for connection in self.connections:

            if connection.handle_packet(packet):
                accepted = True
                break
        else:

            # Check if it is udp for a new connection
            if ("UDP" in packet and "DNS" not in packet and "SSDP" not in packet and "NBNS" not in packet 
                and "DHCP" not in packet and "SMB" not in packet and "MDNS" not in packet and "NTP" not in packet 
                and "DHCPV6" not in packet and "LMNR" not in packet and "QUIC" not in packet and "ICMPV6" not in packet 
                and "ICMP" not in packet and "STUN" not in packet and packet.udp.port != "443"):

                # Make a new connection
                new_conn = conn.Connection(f"Application Connection {self.conn_num}", get_dst(packet), [get_src(packet)], float(packet.sniff_timestamp))
                self.connections.append(new_conn)

                # Increase conn_num for application naming
                self.conn_num += 1

                # set accepted
                accepted = True

        # Return out of void
        return accepted

    def __str__(self) -> str:

        output = "App Tracker Module:<br />"

        for connection in self.connections:
            output += str(connection) + "<br />"

        output += "Dead Connections:<br />"

        for connection in self.dead_connections:
            output += str(connection) + "<br />"
        
        return output