import pyshark.packet.packet as pypacket

def get_src(packet: pypacket.Packet) -> str:

    try:
        return packet.ip.src
    except:
        try:
            return packet.wlan_aggregate.ip_src
        except:
            print("ip_src access failure")
            return ""
        
def get_dst(packet: pypacket.Packet) -> str:

    try:
        return packet.ip.dst
    except:
        try:
            return packet.wlan_aggregate.ip_dst
        except:
            print("ip_dst access failure")
            return ""