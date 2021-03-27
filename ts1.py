# Abdulrahman Abdulrahman (aa1684) and Manav Patel (mjp430)
import socket
import sys


# Opens file and gets all ip addresses needed
# Stores it in db dictionary
def read_dnsts():
    file = open('PROJI-DNSTS1.txt', 'r')
    database = file.readlines()
    db = {}

    for line in database:
        list = line.strip('\n').split(" ")
        db[list[0].lower()] = list[1]

        # print(db)
    return db


def tserver():
    # Make sure we have a port number
    if len(sys.argv) != 2:
        print("Error: Please use the proper command: python ts1.py ts1ListenPort")
        exit()

    HOST = "0.0.0.0"
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print("Error: Please ensure you are using proper Ports")
        exit()

    # Get DNS file
    db = read_dnsts()

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    ss.bind((HOST, PORT))
    ss.listen(1)

    while True:
        conn, addr = ss.accept()
        print("Connected to ", addr)

        # with conn:
        data = conn.recv(1024).decode("utf-8")
        print(data)
        # Checks in our dictionary, if not sends the localhost
        if data in db:
            conn.sendall(str.encode(db[data]))
        else:
            conn.sendall(b'NS')


if __name__ == "__main__":
    tserver()