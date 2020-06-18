import socket

def send_recv(conn,cmd):
    HEADERSIZE = 10
    conn.send(str.encode(cmd,'utf-8'))
    full_msg = ''
    # while True:       # These codes will work but to break the revc from recving we need to close the connecetion from remort
    #     output = conn.recv(10)  # NOT IDEAL in thise case as we need the stream to continue
    #     if len(output) <= 0:
    #         break
    #     full_msg = full_msg + output.decode('utf-8')
    """
        # using a header field to (here just the HEADERSIZE) to pass the message length to our code ,No .close() is required
        form the remote end
    """
    new_msg = True
    while True:
        # print('waiting')
        msg = conn.recv(1024)
        # print('msg found')
        if new_msg:
            msglen = int(msg[:HEADERSIZE].strip())
            new_msg = False
        full_msg = full_msg + msg.decode('utf-8')
        # print(full_msg,len(full_msg)-HEADERSIZE)
        if (len(full_msg) - HEADERSIZE) == msglen:
            break

    # print(full_msg)
    return full_msg[HEADERSIZE:]

def get_connection(soc_obj):
    conn , add = soc_obj.accept()
    return conn, add


def create_soc(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(3)
    return s

def isalive(conn):
    try:
        # ping = "ping {} -p {}".format(conn[1][0],conn[1][1])
        conn.send(str.encode('hi'))
        conn.recv(1024)
        # conn.send(str.encode('hello'))

        return True
    except:
        return False
