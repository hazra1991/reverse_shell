import threading,signal
from time import sleep
import socket ,subprocess
from soc_fun import create_soc, send_recv,get_connection,isalive

conn_pool = []
thread_pool= ['t1','t2']        #this variable can be changed in the global space as its a mutable one
SERVER_ALIVE = True
# HOST='192.168.29.78'
HOST=socket.gethostname()
PORT=1234

# TODO :- if no stdout at client it should be handeled by sending the cwd/pwd

# TODO :- send ,Rceive and excecute features should be added to the server and client codes :

class TerminalThread(threading.Thread):

    '''Inherited Thread class and implemented custom run().Here the threads features are extended'''

    def __init__(self,get_pool,get_chanel,check_ip,quit=None):
        self.get_pool = get_pool
        self.get_chanel = get_chanel
        self.check_ip = check_ip
        threading.Thread.__init__(self)

    def run(self):
        print('\n\t\t-------------------------------------------------------------------------------')
        print("\t\tTerminal commands :- 'list' ,'connect <chanel ID>, grep <Ip Address>'quit'\n\t\tEnter 'list to get all the chanel IDs corresponding to ip connection\n")
        print('\t\t-------------------------------------------------------------------------------\n\n\n')
        while True:
            tcmd = input('\nShell>').strip().lower()
            try:
                tcmd = tcmd.split()
                if 'list' in tcmd and len(tcmd) == 1 :
                    self.get_pool()
                elif len(tcmd) == 2 and 'grep' in tcmd:
                    if _check_ip(tcmd[1]):
                        given_ip = tcmd[1].strip()
                        for i in conn_pool:
                            if i[1][0] == given_ip:
                                print('Ip {} port {}  channel ID ::- {}'.format(given_ip,i[1][1],conn_pool.index(i)))
                    else:
                        print('Specify a proper ip address')


                elif len(tcmd) == 2 and 'connect' in tcmd:
                    chanel_ID = int(tcmd[1])
                    if chanel_ID >= 0:
                        self.get_chanel(chanel_ID)
                        # print(chanel_ID)
                    else:
                        raise ValueError

                elif 'quit' in tcmd and len(tcmd) == 1:
                    global SERVER_ALIVE          # need to refer global as it is outside the scope of this class
                    SERVER_ALIVE = False         # if not then will reassing teh value agin in this scope ,and not changing it on global scope
                    exit(0)

                else:
                    print('provide a proper command format')
            except ValueError:
                print('Please enter a valied chanel ID')
            except IndexError:
                print('No client connected')

class ConnectionThread(threading.Thread):

    # Threading implemented by overwriding run() and adding a exit functionality
    def run(self):
        try:
            self.so = create_soc(HOST,PORT)
            while True:
                conn,add = get_connection(self.so)
                # s = send_recv(conn,'netstat -a -n')
                # print(s)
                conn_pool.append((conn,add))
        except OSError:
            print('connection error ... exiting ')
            exit(0)

    def exit(self):
        for i in conn_pool:
            # i[0].shutdown(socket.SHUT_RDWR)
            i[0].close()
        self.so.shutdown(socket.SHUT_RDWR)              # Tearing down the connection and socet obj forecefully
        print('shutdown')
        self.so.close()
        exit(0)




def _get_chanel(chanel_id):

    ## Connect to a client

    conn,add =  conn_pool[chanel_id]
    try:

        if isalive(conn):
            print("{:^150}\n{}\nconnected to {} on {}".format('******This is an interactive terminal simulator shell*******','\t\t\t\tfile open commands and application oporation such as top is not available (WIP)',add[0],add[1]))
            while True:
                cmd = input('@{}:{}>'.format(add[0],add[1]))
                if cmd == 'exit':
                    return
                if len(cmd) > 0:
                    client_msg =  send_recv(conn,cmd)
                    print(client_msg,end='')
                elif len(cmd) == 0:
                    client_dir = send_recv(conn,'\n')
                    print(client_dir , end='')


        else:
            print("unnable to connect . Thread dead")
            _remove_conn(conn_pool[chanel_id])
    except ValueError:
        print("unnable to connect . Thread dead")
        _remove_conn(conn_pool[chanel_id])
    except BrokenPipeError:
        print("unnable to connect . Thread dead")
        _remove_conn(conn_pool[chanel_id])


def _get_pool():
    # pulls and refresshes the connected hosts
    if len(conn_pool) > 0:
        print('-----------connected Client list-------------\nIP\t\tPORT\t\tchannel ID')
        for i in conn_pool:
            conn ,add = i
            if isalive(conn):
                print("{}\t{}\t\t{} ".format(add[0],add[1],conn_pool.index(i)))
            else:
                _remove_conn(i)
    else:
        print("No client conencted")

def _check_ip(ip):
    try:
        ip_list = ip.strip().strip("\n").split(".")
        if len(ip_list) == 4 :
            for i in ip_list:
                if " " in i or int(i)>255 or int(i) < 0 or '+' in i:
                    raise ValueError
            return True
    except ValueError:
        return False

def _remove_conn(element):
    temp = conn_pool.index(element)
    conn_pool.pop(temp)


def _keepalive():
    while SERVER_ALIVE:
        sleep(6)
        for e in conn_pool:
            isalive(e[0])
    return

if __name__=="__main__":

    '''
        # TODO create another thread for keepalive .
    '''
    thread_pool[0] = ConnectionThread()  # run in one
    thread_pool[1] = TerminalThread(_get_pool,_get_chanel,_check_ip)
    thread_pool[0].start()
    thread_pool[1].start()
    # _keepalive()
    thread_pool[1].join()
    print("{:^100}".format('********* Exiting Server ************\n\n\n\n'))
    thread_pool[0].exit()
    # print("**************** Exiting Server ******************* ")
