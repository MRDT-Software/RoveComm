import json
import sys


# Define some c specific #defines and file header
define_prefix = "#define"
header = """#ifndef RoveCommManifest_h
#define RoveCommManifest_h

#include <stdint.h>
#include\"RoveCommPacket.h\"

"""

# Maps types from json to c types
type_to_ctype = {
    "INT8_T": "int8_t",
    "UINT8_T": "uint8_t",
    "INT16_T": "int16_t",
    "UINT16_T": "uint16_t",
    "INT32_T": "int32_t",
    "UINT32_T": "uint32_t",
    "FLOAT_T": "float",
    "DOUBLE_T": "double",
    "CHAR": "char",
}

this = sys.modules[__name__]

this.manifest = None
this.manifest_file = None
this.header_file = None


def insert_packets(board, type):
    """
    This inserts all Ids for a given type (Command, Telemetry, Error)
    Currently adds the comments, dataId, dataCount and dataType
    """
    if (type in this.manifest[board] and len(this.manifest[board][type]) > 0):
        messages = this.manifest[board][type]
        this.header_file.write(f"////////////////////{type}\n")

        for message in messages:
            print(message)
            dataId = this.manifest[board][type][message]["dataId"]
            dataCount = this.manifest[board][type][message]["dataCount"]
            comments = this.manifest[board][type][message]["comments"]

            # Data type doesn't exactly match the c type
            dataType = this.manifest[board][type][message]["dataType"]
            dataType = type_to_ctype[dataType]

            this.header_file.write(f"//{comments}\n")
            this.header_file.write(
                f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_'+message.upper()+'_DATA_ID':<80}{dataId:<10}\n"
            )
            this.header_file.write(
                f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_'+message.upper()+'_DATA_COUNT':<80}{dataCount:<10}\n"
            )
            this.header_file.write(
                f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_'+message.upper()+'_DATA_TYPE':<80}{dataType:<10}\n"
            )
            this.header_file.write("\n")

def insert_enums(board):
    if ("Enums" in this.manifest[board]):
        enums = this.manifest[board]["Enums"]
        this.header_file.write(f"////////////////////Enums\n")
        for enum in enums:
            this.header_file.write(f"{'enum ' + board.upper() + 'BOARD' + '_' + enum.upper() + ' {'}")
            output = ""
            for value in enums[enum]:
                print(value)
                output += f"{value.upper() + ','}"
            output = output[:-1] #Removing "," from the last element of the enum 
            this.header_file.write(f"{output + '};'} \n")

if __name__ == "__main__":
    # Load the json file
    this.manifest_file = open("../manifest/manifest.json", "r").read()
    this.manifest_file = json.loads(this.manifest_file)

    # Check manifest spec version
    if this.manifest_file["ManifestSpecVersion"] != 3:
        print("Expected Manifest Spec v3, Aborting")
        exit()

    # Manifest contains additional info not necessary for header file
    this.manifest = this.manifest_file["RovecommManifest"]
    this.header_file = open("RoveCommManifest.h", "w")
    this.header_file.write(header)

    # Write all the Ips and Ports together
    for board in this.manifest:
        ip = this.manifest[board]["Ip"]
        ip_octs = ip.split(".")

        # The < character indicates something is left aligned, in this case we are assuming that the name
        # plus #define is less than or equal to 50 characters and the PORT/IP less than 10
        this.header_file.write(
            f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_FIRSTOCTET':<60}{ip_octs[0]:<10}\n"
        )
        this.header_file.write(
            f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_SECONDOCTET':<60}{ip_octs[1]:<10}\n"
        )
        this.header_file.write(
            f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_THIRDOCTET':<60}{ip_octs[2]:<10}\n"
        )
        this.header_file.write(
            f"{define_prefix + ' RC_'+board.upper()+'BOARD'+'_FOURTHOCTET':<60}{ip_octs[3]:<10}\n"
        )
        this.header_file.write("\n")

    # A couple of newlines between IP assignments and rovecomm messages
    this.header_file.write("\n\n")

    # Insert the update rate and UDP port
    this.update_rate = this.manifest_file["updateRate"]
    this.header_file.write(f"{define_prefix + ' ROVECOMM_UPDATE_RATE':<60}{this.update_rate:<10}\n")

    this.udp_port = this.manifest_file["ethernetUDPPort"]
    this.tcp_port = this.manifest_file["ethernetTCPPort"]
    this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_ETHERNET_UDP_PORT':<60}{this.udp_port:<10}\n")
    this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_ETHERNET_TCP_PORT':<60}{this.tcp_port:<10}\n")

    # Also grab the first 3 octets of the subnet IP
    # this.subnet_ip = this.manifest_file["subnetIP"]
    # this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_SUBNET_IP_FIRST_OCTET':<60}{this.subnet_ip[0]:<10}\n")
    # this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_SUBNET_IP_SECOND_OCTET':<60}{this.subnet_ip[1]:<10}\n")
    # this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_SUBNET_IP_THIRD_OCTET':<60}{this.subnet_ip[2]:<10}\n")

    this.header_file.write("\n\n")

    # Grabs the first 5 bytes of the MAC address
    this.subnet_mac = this.manifest_file["MACaddressPrefix"]
    this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_SUBNET_MAC_FIRST_BYTE':<60}{this.subnet_mac[0]:<10}\n")
    this.header_file.write(f"{define_prefix + ' RC_ROVECOMM_SUBNET_MAC_SECOND_BYTE':<60}{this.subnet_mac[1]:<10}\n")

    this.header_file.write("\n\n")

    # First insert the reserved System Id's
    this.system_packets = this.manifest_file["SystemPackets"]
    this.header_file.write(f"///////////////////////////////////////////////////\n")
    this.header_file.write(f"{'////////////':<20}{'System Packets':<20}{'///////////':<20}\n")
    this.header_file.write(f"///////////////////////////////////////////////////\n\n")

    for packet in this.system_packets:
        this.header_file.write(
            f"{define_prefix + ' RC_ROVECOMM_'+packet.upper()+'_DATA_ID':<60}{this.system_packets[packet]:<10}\n"
        )
    this.header_file.write("\n\n")

    # Now go through and write all the commands and telemetry
    for board in this.manifest:
        this.header_file.write(f"///////////////////////////////////////////////////\n")
        this.header_file.write(f"{'////////////':<20}{board.upper()+'BOARD':<20}{'///////////':<20}\n")
        this.header_file.write(f"///////////////////////////////////////////////////\n\n")

        # Insert the commands, telemetry and error messages for this particular board
        insert_packets(board, "Commands")
        insert_packets(board, "Telemetry")
        insert_packets(board, "Error")
        insert_enums(board)

        # Write a couple of newlines to seperate boards
        this.header_file.write("\n\n")

    this.header_file.write("#endif // RoveCommManifest_h")
    this.header_file.close()
