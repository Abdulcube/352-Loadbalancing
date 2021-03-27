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
        # Make sure our ports are integers
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

        # Send the host name for DNS lookup
        cs.connect((AHOST, PORT))
        cs.sendall(str.encode(query))

        # Receive lookup from LS
        data = cs.recv(1024)
        code = data.decode("utf-8").split(" ")

        # If found in RS, write to RESOLVED.txt, else continue lookup in TS
        if code[1] == "A":
            resolved.write(query + " " + code[0] + " A\n")
            print(query + " - " + code[0] + " A")
        else:
            # If the code received wasn't "A", then the host wasn't found in any server
            resolved.write(query + " - " + "Error:HOST NOT FOUND\n")
            print(query + " - " + "Error:HOST NOT FOUND")
    print("Done")


if __name__ == "__main__":
    client()
