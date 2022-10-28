import socket
import subprocess
import time

HOST = '172.16.1.54'  
PORT = 9009

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)

def desligarasp():
    comando = "/usr/bin/sudo /sbin/shutdown -h now"
    print(comando)
    time.sleep(3)
    import subprocess
    processo = subprocess.Popen(comando.split(), stdout=subprocess.PIPE)
    output = processo.communicate()[0]
    print(output)
      
while True:
    try:
        msg, cliente = udp.recvfrom(1024)
        if msg.decode() == 'desliga':
            desligarasp()
        else:
            print(cliente, msg.decode())
    except Exception as e:
        print(e)
        udp.close()
        break
udp.close()
