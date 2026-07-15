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
    PayloadA2S_Info : bytes = bytearray() 

    # Writing the value -1 as long type (signed int) 4 Bytes
    PayloadA2S_Info += struct.pack("<l", -1)

    # Writing a static line of string bytes to our payload
    PayloadA2S_Info += b'TSource Engine Query\0' 

    # Static payload
    # PayloadA2S_Info : bytes = b'\xff\xff\xff\xffTSource Engine Query\0'
    
    # Sending our payload to the server using the current socket
    sock.sendto(PayloadA2S_Info, server)

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