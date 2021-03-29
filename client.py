# Abdulrahman Abdulrahman (aa1684) and Manav Patel (mjp430)
import socket
import os
import sys


def client():
    # Check if we have the proper arguments
    if len(sys.argv) != 3:
        print("Error: Please use the proper command: python client.py lsHostname lsListPort")
        exit()

    # Read the list of domains
    file = open('PROJ2-HNS.txt', 'r')
    queries = file.readlines()
    print(queries)

    # If RESOLVED.txt previously existed, remove it so we can create and append to a new file
    try:
        os.remove("RESOLVED.txt")
    except OSError:
        pass
    resolved = open("RESOLVED.txt", "a")

    # Loop through each domain name and connect to our rs and/or ts for DNS lookups
    for line in queries:
        query = line.strip('\n').lower()
        """HOST = '127.0.0.1'
        PORT = 26844"""

        HOST = sys.argv[1]
        # Make sure our port is an integer
        try:
            PORT = int(sys.argv[2])
        except ValueError:
            print("Error: Please ensure you are using proper Ports")
            exit()

        # Connect to the LS
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            AHOST = socket.gethostbyname(HOST)
            # print("[C]: Client socket created")
        except socket.error as err:
            print('socket open error: {} \n'.format(err))
            exit()
    
        # Connect to the LS Server
        cs.connect((AHOST, PORT))

        # Send the host name for DNS lookup
        cs.sendall(str.encode(query))

        # Receive lookup from LS
        data = cs.recv(1024)
        code = data.decode("utf-8").split(" ")

        # print("Here is the data " + data)
        
        # Write our results to the output file
        if data == "NS":
            resolved.write(query + " - " + "Error:HOST NOT FOUND\n")
            print(query + " - " + "Error:HOST NOT FOUND")
        else:
            # If the data received wasn't "NS" then we found a match, write to file
            resolved.write(query + " " + code[0] + " A\n")
            print(query + " - " + code[0] + " A")
    print("Done")


if __name__ == "__main__":
    client()
