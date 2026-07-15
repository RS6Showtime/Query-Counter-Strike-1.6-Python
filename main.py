# Importing libraries into our script.
import socket
import struct
import argparse

# A function we will use later to parse strings from a linear bytes
def read_string(data : bytes, offset : int) -> str:
    end = data.index(b"\x00", offset)
    text = data[offset:end].decode("utf-8", errors="replace")
    return text, end + 1

def ReadNewSourceQuery(data : bytes, offset : int) -> None:
    Protocol, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    Hostname, offset = read_string(data, offset) # String
    Map, offset = read_string(data, offset) # String
    Folder, offset = read_string(data, offset) # String
    Game, offset = read_string(data, offset) # String

    AppID, = struct.unpack_from("<h", data, offset) # Short
    offset += 2

    Players, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    MaxPlayers, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    Bots, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    ServerType, = struct.unpack_from("<c", data, offset) # Char
    offset += 1

    Environment, = struct.unpack_from("<c", data, offset) # Char
    offset += 1

    Visibility, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    VAC, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    Version, offset = read_string(data, offset) # String

    Flags, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    print(f"Protocol: {Protocol}")
    print(f"Hostname: {Hostname}")
    print(f"Map: {Map}")
    print(f"Folder: {Folder}")
    print(f"Game: {Game}")
    print(f"AppID: {AppID}")
    print(f"Players: {Players}")
    print(f"MaxPlayers: {MaxPlayers}")
    print(f"Bots: {Bots}")

    if ServerType == b'd':
        print("ServerType: Dedicated Server")
    elif ServerType == b'l':
        print("ServerType: Non-Dedicated Server")
    elif ServerType == b'p':
        print("ServerType: Proxy HLTV")

    if Environment == b'l':
        print(f"Environment: Linux")
    elif Environment == b'w':
        print(f"Environment: Windows")
    elif Environment == b'm' or Environment == b'o':
        print(f"Environment: Mac")

    if Visibility == 0:
        print("Visibility: No-Password Required")
    else:
        print("Visibility: Require Password")

    print(f"VAC: {bool(VAC)}")
    print(f"Version: {Version}")

    # The server sent the server port
    if Flags & 0x80:
        ServerPort, = struct.unpack_from("<h", data, offset) # Short
        offset += 2

        print(f"ServerPort: {ServerPort}")

    if Flags & 0x10:
        SteamID, = struct.unpack_from("<q", data, offset) # Long long
        offset += 8

        print(f"SteamID: {SteamID}")

    # For Hltv
    if Flags & 0x40:
        HLTVPort, = struct.unpack_from("<h", data, offset) # Short
        offset += 2

        Name, offset = read_string(data, offset) # String

        print(f"HLTVPort: {HLTVPort}")
        print(f"Name: {Name}")

    if Flags & 0x20:
        Keywords, offset = read_string(data, offset) # String

        print(f"Keywords: {Keywords}")

    if Flags & 0x01:
        GameID, = struct.unpack_from("<q", data, offset) # Long Long
        offset += 8

        print(f"GameID: {GameID}")

def ReadOldSourceQuery(data : bytes, offset : int) -> None:
    Address, offset = read_string(data, offset) # String
    Hostname, offset = read_string(data, offset) # String
    Map, offset = read_string(data, offset) # String
    Folder, offset = read_string(data, offset) # String
    Game, offset = read_string(data, offset) # String

    Players, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    MaxPlayers, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    Protocol, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    ServerType, = struct.unpack_from("<c", data, offset) # Char
    offset += 1

    Environment, = struct.unpack_from("<c", data, offset) # Char
    offset += 1

    Visibility, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    print(f"Protocol: {Protocol}")
    print(f"Address: {Address}")
    print(f"Hostname: {Hostname}")
    print(f"Map: {Map}")
    print(f"Folder: {Folder}")
    print(f"Game: {Game}")
    print(f"Players: {Players}")
    print(f"MaxPlayers: {MaxPlayers}")

    if ServerType == b'D':
        print("ServerType: Dedicated Server")
    elif ServerType == b'L':
        print("ServerType: Non-Dedicated Server")
    elif ServerType == b'P':
        print("ServerType: Proxy HLTV")

    if Environment == b'L':
        print(f"Environment: Linux")
    elif Environment == b'W':
        print(f"Environment: Windows")

    if Visibility == 0:
        print("Visibility: No-Password Required")
    else:
        print("Visibility: Require Password")

    Mod, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    if Mod == 1:
        print("Mod: Half-Life (Custom)")

        Link, offset = read_string(data, offset) # String
        DownloadURL, offset = read_string(data, offset) # String

        NULL, = struct.unpack_from("<b", data, offset) # Byte ? Is this NULL as the valve say or a null terminator from DW-url?
        offset += 1

        ModVersion, = struct.unpack_from("<l", data, offset) # Long
        offset += 4

        Size, = struct.unpack_from("<l", data, offset) # Long
        offset += 4

        Type = struct.unpack_from("<b", data, offset) # Long
        offset += 1

        DLL = struct.unpack_from("<b", data, offset) # Long
        offset += 1

        print(f"Link: {Link}")
        print(f"DownloadURL: {DownloadURL}")
        print(f"NULL: {NULL}")
        print(f"ModVersion: {ModVersion}")
        print(f"Size: {Size}")

        if Type == 1:
            print("Type: For Multiplayer only")
        else:
            print("Type: For SinglePlayer & Multiplayer")

        if DLL == 1:
            print("DLL: Using Original")
        else:
            print("DLL: Using Custom")
    else:
        print("Mod: Half-Life (default)") 

    VAC, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    Bots, = struct.unpack_from("<b", data, offset) # Byte
    offset += 1

    print(f"VAC: {bool(VAC)}")
    print(f"Bots: {Bots}")

def ReadPlayers(data : bytes, offset : int) -> None:
    TotalPlayers, = struct.unpack_from(b"<b", data, offset)
    offset += 1

    print(f"TotalPlayers: {TotalPlayers}")

    print("Players List:")
    print("--------------------------")

    for i in range(TotalPlayers):
        Index, = struct.unpack_from("<b", data, offset) # Byte
        offset += 1

        Name, offset = read_string(data, offset)

        Score, = struct.unpack_from("<l", data, offset) # Long
        offset +=4

        Duration, = struct.unpack_from("<f", data, offset) # Long
        offset += 4

        print(f"Index: {Index}")
        print(f"Name: {Name}")
        print(f"Score: {Score}")
        print(f"Duration: {Duration}")
        print("--------------------------")

def ReadRules(data : bytes, offset : int) -> None:
    TotalRules, = struct.unpack_from(b"<h", data, offset)
    offset += 2

    print(f"TotalRules: {TotalRules}")

    print("Rules List:")
    print("--------------------------")

    for i in range(TotalRules):
        Name, offset = read_string(data, offset)
        Value, offset = read_string(data, offset)

        print(f"Name: {Name}")
        print(f"Value: {Value}")
        print("--------------------------")

# Snipped from my project MXP-RBOT (An emulated CS 1.6 project)
# x10 Better than xfakeplayers 
def HandleReadFragmentsOOB(sock : socket.socket, data : bytes, offset : int) -> bytes:
    fragments = {}
    
    sequence_num, = struct.unpack_from("<l", data, offset)
    offset += 4

    packet_id, = struct.unpack_from("<b", data, offset)
    offset += 1

    packet_count = packet_id & 0x0F
    packet_number = (packet_id >> 4)
    
    fragments[packet_number] = data[offset:]

    while len(fragments) < packet_count:
        try:
            packet, _ = sock.recvfrom(1400)
        except socket.timeout:
            print("Timeout occured")
            break

        offset = 0
        oob_header, = struct.unpack_from("<l", packet, offset)
        offset += 4

        if oob_header == -2:
            seq, = struct.unpack_from("<l", packet, offset)
            offset += 4

            p_id, = struct.unpack_from("<b", packet, offset)
            offset += 1

            p_count = p_id & 0x0F
            p_num = (p_id >> 4)

            if seq == sequence_num:
                fragments[p_num] = packet[offset:]

    fullMsg = bytearray()
    for i in range(packet_count):
        if i in fragments:
            fullMsg += fragments[i]
        else:
            print(f"Error, missing fragment {i}!")
            return b""

    return bytes(fullMsg)

def HandleResponses(sock : socket.socket, data : bytes) -> None:
    # We use offset to know where to start with the read (index)
    # Offset's will increment based on the size of the datatype we used to read
    offset : int = 0

    OOB, = struct.unpack_from("<l", data, 0) # Long | Should be -1
    offset += 4

    # More Context
    if OOB == -2:
        data = HandleReadFragmentsOOB(sock, data, offset)

        # Recall it will full received data
        # We do not require socket here
        HandleResponses(None, data) 
        return

    # We can check if the OOB is -1
    elif OOB != -1:
        print("The OOB value from the server is not the right one.")
        return
    
    Header, = struct.unpack_from("<c", data, offset) # Char
    offset += 1

    # Handling response when the header is 'I"
    if Header == b'I':
        ReadNewSourceQuery(data, offset)
    # Another header called "Obsolete GoldSource Response"
    elif Header == b'm':
        ReadOldSourceQuery(data, offset)
    elif Header == b'D':
        ReadPlayers(data, offset)
    elif Header == b'E':
        ReadRules(data, offset)

# Program main function
def main(server : list) -> None:
    # Initializing a socket class.
    # AF_INET is used to initialize a socket which will use Internet Protocol (IP).
    # SOCK_DGRAM is used to communicate with the host using the UDP.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # # Setting up a payload so we can start and query for server information.
    # # In counter-strike 1.6 this is also called A2S_INFO
    PayloadA2S_INFO = b'\xff\xff\xff\xffTSource Engine Query\0'
    
    # Sending the query payload to the server
    sock.sendto(PayloadA2S_INFO, server)

    # Waiting the server with a response for the server with the data we fighted for!
    data, _ = sock.recvfrom(1400)
    HandleResponses(sock, data)
    
    # Now, we will get the players list (A2S_PLAYER)
    # For this, we need to provide to the server a challenge code.
    # We can obtain it by asking the server and then use it when we query for the players

    # We will initialize a new socket, because we might still have data on the queue and we don't want it
    # This can happen when the server sent old query A2S_INFO and will also send new query A2S_INFO
    # Close old socket
    sock.close()

    # Initialize a new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    PayloadChallengeRequestForA2S_PLAYER = b'\xFF\xFF\xFF\xFF\x55\xFF\xFF\xFF\xFF'

    # Sending the payload to the server
    sock.sendto(PayloadChallengeRequestForA2S_PLAYER, server)

    # Waiting for data
    data, _ = sock.recvfrom(1400)

    print(data)
    
    # Not a valid challenge code response
    # The response is something like this: \xff\xff\xff\xffA"Q\x88H
    if not data.startswith(b'\xff\xff\xff\xffA'):
        print("Invalid challenge code reposense.")
        return
    
    # Now, we have the challenge code
    ChallengeCode, = struct.unpack_from("<l", data, 5) # Long
    
    # We are free to ask for full A2S_PLAYER
    PayloadA2S_PLAYER = b'\xff\xff\xff\xff\x55' + ChallengeCode.to_bytes(4, byteorder='little', signed=True)

    # Sending the payload
    sock.sendto(PayloadA2S_PLAYER, server)

    # Waiting for response
    data, _ = sock.recvfrom(1400)

    if not data.startswith(b'\xff\xff\xff\xff'):
        print("Not a valid OOB on A2S_PLAYER")
        return

    # Handling responses (It will handle A2S_PLAYER)
    HandleResponses(sock, data)

    # Asking the same, the challenge code, but now for A2S_RULES
    # (Well, we don't really have to ask again for the challenge code, because it might be the same
    # ,but due to lag or delay it might change in that frame)
    PayloadChallengeRequestForA2S_RULES = b'\xFF\xFF\xFF\xFF\x56\xFF\xFF\xFF\xFF'

    # Sending the payload to the server
    sock.sendto(PayloadChallengeRequestForA2S_RULES, server)

    # Waiting for data
    data, _ = sock.recvfrom(1400)
    
    # Not a valid challenge code response
    # The response is something like this: \xff\xff\xff\xffA"Q\x88H
    if not data.startswith(b'\xff\xff\xff\xffA'):
        print("Invalid challenge code reposense.")
        return
    
    # Now, we have the challenge code
    ChallengeCode, = struct.unpack_from("<l", data, 5) # Long

    # We are free to ask for full A2S_RULES
    PayloadA2S_RULES = b'\xff\xff\xff\xff\x56' + ChallengeCode.to_bytes(4, byteorder='little', signed=True)

    # Sending the payload
    sock.sendto(PayloadA2S_RULES, server)

    # Waiting for response
    data, _ = sock.recvfrom(1400)

    # Handling responses (It will handle A2S_RULES)
    HandleResponses(sock, data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Query Counter-Strike 1.6", description="Querying Counter-strike 1.6 Informations")

    parser.add_argument("--server", required=True, help="Server IP:Port")

    args = parser.parse_args()
    Host : str = args.server

    SplitedServer = Host.split(":")

    server = (SplitedServer[0], int(SplitedServer[1]))

    main(server)