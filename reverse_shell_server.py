import threading
import socket ,subprocess
from soc_fun import create_soc, send_recv,get_connection,isalive
conn_pool = []
thread_pool= ['t1','t2']
HOST=socket.gethostname()
PORT=1234

class TerminalThread(threading.Thread):

    def __init__(self,get_pool,get_chanel,check_ip,quit=None):
        self.get_pool = get_pool
        self.get_chanel = get_chanel
        self.check_ip = check_ip
        threading.Thread.__init__(self)

    def run(self):
        print("\n\t\tTerminal commands :- 'list' ,'connect <chanel ID>, 'quit'\n\t\tEnter 'list to get all the chanel IDs corresponding to ip connection\n")
        while True:
            tcmd = input('$>').strip().lower()
            try:
                tcmd = tcmd.split()
                if 'list' in tcmd and len(tcmd) == 1 :
                    self.get_pool()
                elif len(tcmd) == 2 and 'grep' in tcmd:
                    if self.check_ip(tcmd[1]):
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
                    # TODO need to redo the Exiting
                    exit()

                else:
                    print('provide a proper command format')
            except ValueError:
                print('Please enter a valied chanel ID')
            except IndexError:
                print('No client connected')



def _get_chanel(chanel_id):

    conn,add =  conn_pool[chanel_id]

    if isalive(conn):
        print("{:^150}\n{}\nconnected to ip socket on {}".format('******This is an interactive shell*******','file open commands and application oporation such as top is not available (WIP)',add))
        while True:
            cmd = input('~>')
            if cmd == 'exit':
                return
            if len(cmd) > 0:
                client_msg =  send_recv(conn,cmd)
                print(client_msg,end='')
            elif len(cmd) == 0:
                client_dir = send_recv(conn,'pwd')
                print(client_dir , end='')


    else:
        print("unnable to connect . Thread dead")
        temp = conn_pool.index(conn_pool[chanel_id])
        conn_pool.pop(temp)


def _get_pool():
    if len(conn_pool) > 0:
        for i in conn_pool:
            conn ,add = i
            if isalive(conn):
                print("Ip {} port {}  channel ID ::- {} ".format(add[0],add[1],conn_pool.index(i)))
            else:
                temp = conn_pool.index(i)
                conn_pool.pop(temp)
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

def main():
    try:
        so = create_soc(HOST,PORT)
        while True:
            conn,add = get_connection(so)
            # s = send_recv(conn,'netstat -a -n')
            # print(s)
            conn_pool.append((conn,add))
    except:
        exit(0)

if __name__=="__main__":

    '''
        # TODO create another thread for keepalive .
    '''
    thread_pool[0] = threading.Thread(target=main)  # run in one threading
    thread_pool[1] = TerminalThread(_get_pool,_get_chanel,_check_ip)
    thread_pool[0].start()
    thread_pool[1].start()
    # thread_pool[1].join()
    # print("Exiting programm")