from math import floor
from time import strftime, localtime
import pyshark.packet.packet as pypacket

class Connection:

    def __init__(self, name: str, user_ip: str, server_ips: list[str], start_time: float):

        # Setup variables
        self.names = [name]
        self.user_ip = user_ip
        self.server_ips = server_ips

        # Constant starting variables
        self.end_time = 0
        self.volume = 0
        self.packet_count = 0
        
        # Set start time
        self.start_time = floor(start_time)

    def accept_packet(self, packet: pypacket.Packet) -> None:

        # update end time
        self.end_time = floor(float(packet.sniff_timestamp))

        # probably increase length correctly TODO: Check this
        self.volume += len(packet)

        # Increase packet count
        self.packet_count += 1

    def expand_server_ips(self, new_ips: list[str]) -> None:

        # Add new ips to the server ips list
        for ip in new_ips:
            if ip not in self.server_ips:
                self.server_ips.append(ip)

    def expand_name(self, new_name: str) -> None:

        # Add the new name if necessary
        if new_name not in self.names:
            self.names.append(new_name)

    # Return whether or not a packet is part of our connection
    def is_ours(self, packet: pypacket.Packet) -> bool:

        return (packet.ip.src in self.server_ips)
    
    # Check if a packet should be considered a new connection for us
    def is_new_connection(self, packet: pypacket.Packet) -> bool:

        # If this is a dns query, check if it has the same name as us
        if "DNS" in packet:
            return packet.dns.qry_name in self.names and ((floor(float(packet.sniff_timestamp)) - (self.end_time if self.end_time > self.start_time else self.start_time)) >= 300)
        else: # Otherwise just check the ip
            return packet.ip.src in self.server_ips and ((floor(float(packet.sniff_timestamp)) - (self.end_time if self.end_time > self.start_time else self.start_time)) >= 300)

    def __str__(self) -> str:

        return f"{self.names}<br />-----Start Time: {self.start_time} ({strftime('%Y-%m-%d %H:%M:%S', localtime(self.start_time))})<br />-----End Time: {self.end_time} ({strftime('%Y-%m-%d %H:%M:%S', localtime(self.end_time))})<br />-----Connection Length (sec): {self.end_time - self.start_time}<br />-----Size Down: {self.volume}<br />-----Server Ips: {self.server_ips}<br />"