# Abdulrahman Abdulrahman (aa1684) and Manav Patel (mjp430)
import socket
import sys
import select


def lserver():
    # Make sure we have a port number
    if len(sys.argv) != 6:
        print("Error: Please use the proper command: python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort")
        exit()

    HOST = "0.0.0.0"
    TS1HOST = sys.argv[2]
    TS2HOST = sys.argv[4]
    try:
        PORT = int(sys.argv[1])
        T1PORT = int(sys.argv[3])
        T2PORT = int(sys.argv[5])
    except ValueError:
        print("Error: Please ensure you are using proper Ports")
        exit()


    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    ss.bind((HOST, PORT))
    ss.listen(1)

    # The client connects to LS here
    #conn, addr = ss.accept()
    #print("Connected to ", addr)

    while True:
        conn, addr = ss.accept()
        print("Connected to ", addr)

        # Read the host name from the client
        data = conn.recv(1024).decode("utf-8")
        data = data.encode('ascii', 'ignore')
        print(data)

        try:
            ct1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ct2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print("[C]: Client socket created")
        except socket.error as err:
            print('socket open error: {} \n'.format(err))
            exit()

        # Check TS1 for the query
        foundT1 = False
        ct1.connect((TS1HOST, T1PORT))
        ct1.sendall(str.encode(data))
        ct1.setblocking(0)

        ready = select.select([ct1], [], [], 5)
        if ready[0]:
            response = ct1.recv(1024)
            print(response)
            conn.sendall(str.encode(response))
            foundT1 = True
        else:
            # conn.sendall(b'NS')
            print("T1 timeout")
        
        # If TS1 did not hold our query, check TS2
        if(foundT1 == False):
            ct2.connect((TS2HOST, T2PORT))
            ct2.sendall(str.encode(data))
            ct2.setblocking(0)

            ready = select.select([ct2], [], [], 5)
            if ready[0]:
                response = ct2.recv(1024)
                print(response)
                conn.sendall(str.encode(response))
            else:
                conn.sendall(b'NS')
                print("T2 timeout")


if __name__ == "__main__":
    lserver()
