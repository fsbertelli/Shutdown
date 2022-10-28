#################################################
#	Author: Felipe Bertelli dos Santos      	#
#	Solinftec - Solutions Development 		#
#	    Version 2.0 - 20/10/2022			#
#################################################

import RPi.GPIO as GPIO
import time
import socket
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#Botao GPIO18
GPIO.setup(24, GPIO.OUT)  #Arduino GPIO24
GPIO.output(24,False)


def desligaMaster():

    with open("/home/solarbot/devices.json") as jf:
        config = json.load(jf)
    for inv in config:
        hostname = inv["hostname"]
        host = inv["host"]
        port = inv["port"]
        try:
    
    #HOST = '172.16.1.131'  
    #PORT = 9009     

            print("[!] Conectado: " + inv["hostname"] + " " + inv["host"])
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dest = (inv["host"], inv["port"])

            msg = ('desliga')
            while msg != '\x18':
                udp.sendto (msg.encode(), dest) 
                udp.close()  
                time.sleep(2)
                print("[!] Enviando comando...")          

        except socket.error as e:
                print ("[!] Erro ao conectar: %s" % e) 
                                
        finally:
                udp.close()               

try:
    while True:
         button_state = GPIO.input(18)
         if button_state == False:
             desligaMaster()
             time.sleep(2)
             print('[!] Desligando devices...')
             time.sleep(1)
             break
finally:
   time.sleep(10)
   print('[!] Desligando PU')
   time.sleep(3)
   GPIO.output(24, True)
   import subprocess
   comando = "/usr/bin/sudo shutdown -h now "
   processo = subprocess.Popen(comando.split(), stdout=subprocess.PIPE)
   time.sleep(2)
   output = processo.communicate()[0]
   print(output)
    
