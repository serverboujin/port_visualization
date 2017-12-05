# -*- coding: utf-8 -*-

import pcapy
from impacket.ImpactDecoder import *
import threading
import Tkinter
import time

TARGET_IP = '192.168.XXX.XXX'
INTERFACE = 'ens33'

# list all the network devices
pcapy.findalldevs()
 
max_bytes = 1024
promiscuous = False
read_timeout = 100 # in milliseconds
pc = pcapy.open_live(INTERFACE, max_bytes, promiscuous, read_timeout)
 
pc.setfilter('ip')  # Filter
 
# callback for received packets
def recv_pkts(hdr, data):
  eth = EthDecoder().decode(data)
  ip = eth.child()
  tcp = ip.child()
  src = ip.get_ip_src()
  try:
    sport = tcp.get_th_sport()
    sport = int(sport)
  except:
    sport = None
  dst = ip.get_ip_dst()
  try:
      dport = tcp.get_th_dport()
      dport = int(dport)
  except:
    dport = None
  print(dport)
  global canvas
  for i in range(5):
    for j in range(5):
      if((dst == TARGET_IP) and (dport == num[j][i])):
        canvas.create_rectangle(i*50+20,j*50+20,i*50+50+20,j*50+50+20,fill='yellow')
        time.sleep(0.2)
        canvas.create_rectangle(i*50+20,j*50+20,i*50+50+20,j*50+50+20,fill='white')
        canvas.create_text(i*50+45,j*50+45,text=num[j][i],font=('FixedSys',10),justify='center')
      elif((dst == TARGET_IP) and (dport != num[j][i])):
        canvas.create_rectangle(4*50+20,4*50+20,4*50+50+20,4*50+50+20,fill='lightgray')
        time.sleep(0.2)
        canvas.create_rectangle(4*50+20,4*50+20,4*50+50+20,4*50+50+20,fill='white')
        canvas.create_text(4*50+45,4*50+45,text=num[4][4],font=('FixedSys',10),justify='center')
      canvas.pack()
      canvas.update()

packet_limit = -1 # infinite

def cap():
  pc.loop(packet_limit, recv_pkts) # capture packets

# Thread to Capture Packets
th = threading.Thread(target=cap)
th.daemon = True
th.start()

#ports = [[0 for i in range(5)] for j in range(5)]
num = [[0 for i in range(5)] for j in range(5)]
# Target Ports
num[0][0] = 20
num[0][1] = 21
num[0][2] = 22
num[0][3] = 23
num[0][4] = 25
num[1][0] = 53
num[1][1] = 67
num[1][2] = 68
num[1][3] = 80
num[1][4] = 110
num[2][0] = 119
num[2][1] = 123
num[2][2] = 137
num[2][3] = 138
num[2][4] = 139
num[3][0] = 143
num[3][1] = 443
num[3][2] = 445
num[3][3] = 587
num[3][4] = 2222
num[4][0] = 3389
num[4][1] = 5900
num[4][2] = 8080
num[4][3] = 50864
num[4][4] = "Other"


root = Tkinter.Tk()
root.title(u"ポート状況")
root.geometry("500x500")
canvas = Tkinter.Canvas(root, width = 500, height = 500)
canvas.place(x=0, y=0)
for i in range(5):
  for j in range(5):
    canvas.create_rectangle(i*50+20,j*50+20,i*50+50+20,j*50+50+20,fill='white')
    canvas.create_text(i*50+45,j*50+45,text=num[j][i],font=('FixedSys',10),justify='center')

root.mainloop()
