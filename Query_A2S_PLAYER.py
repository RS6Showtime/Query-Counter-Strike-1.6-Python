import socket, struct

def main():
    # Initializin a class for our socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    # Checking if the socket we initialized succeded
    if not sock:
        print("Something went wrong while trying to create a socket!")
        return
    
    # Desired Server Tuple
    server : tuple = ("127.0.0.1", 27015)

    # Create an array of bytes using bytearray.
    # We use this, because by using the legacy bytes data type,
    # we might not concat new values to our payload
    PayloadA2S_Player : bytes = bytearray() 

    # Writing the value -1 as long type (signed int) 4 Bytes
    PayloadA2S_Player += struct.pack("<l", -1)

    # Writing a byte (Header) 1 byte
    PayloadA2S_Player += struct.pack("<b", ord("U"))

    # Writing the value -1 as long type (signed int) 4 Bytes
    # Because here we need to specify the ChallengeCode, but
    # because we don't know it, we will ask it from the server!
    PayloadA2S_Player += struct.pack("<l", -1)

    # Static payload
    # PayloadA2S_Player : bytes = b'\xff\xff\xff\xff\x55\xff\xff\xff\xff'
    
    # Sending our payload to the server using the current socket
    sock.sendto(PayloadA2S_Player, server)

    # Waiting for a response from the server
    data, _ = sock.recvfrom(1400)

    # Checking if the server somehow responded to our request, but the page is empty
    if not data:
        print("No data response from the server!")
        return
    
    # Parsing the values using the static structure Valve told us
    OOB, Header, ChallengeCode, = struct.unpack("<lbl", data)

    if Header != ord("A"):
        print(f"Excepting a specific header value, received something unexcepted: {hex(Header)}")
        return
    
    # Now, we have the ChallengeCode, so we can make a request payload as the first one, but
    # we will now include the ChallengeCode in our request
    PayloadA2S_Player : bytes = bytearray() 

    # Writing the value -1 as long type (signed int) 4 Bytes
    PayloadA2S_Player += struct.pack("<l", -1)

    # Writing a byte (Header) 1 byte
    PayloadA2S_Player += struct.pack("<b", ord("U"))

    # Writing the value -1 as long type (signed int) 4 Bytes
    # Because here we need to specify the ChallengeCode, but
    # because we don't know it, we will ask it from the server!
    PayloadA2S_Player += struct.pack("<l", ChallengeCode)

    # Static payload
    # PayloadA2S_Player : bytes = b'\xff\xff\xff\xff\x55' + int.to_bytes(ChallengeCode, 4, byteorder='little', signed=True)

    # Sending our payload to the server using the current socket
    sock.sendto(PayloadA2S_Player, server)

    # Waiting for a response from the server
    data, _ = sock.recvfrom(1400)

    # Checking if the server somehow responded to our request, but the page is empty
    if not data:
        print("No data response from the server!")
        return
    
    # Printing the result!
    print(data)

    # Close the socket
    sock.close()

if __name__ == "__main__":
    main()