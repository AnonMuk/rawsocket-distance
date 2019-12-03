import socket
from datetime import datetime
import auxiliary as ext

TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value

# raw datagram message creation
path = "./results.csv"  # establish constant for results
f = open(path, "w+")
f.write("site,hops,time (msec),matching criteria,IP Matching,Port Matching\n")
f.close()
msg = "measurement for class project; please direct inquiries to student Zubair Mukhi (zxm132@case.edu) or Professor Michael Rabinovich (mxr136@case.edu)"
payload = bytes(msg + "a" * (1472 - len(msg)), "ascii")  # encode payload for dgram
# constants
udp = socket.getprotobyname('udp')
icmp = socket.getprotobyname('icmp')
# Configure sockets
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
senderSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
# using timeout instead of polling. Trying twice at 10 seconds.
recv_sock.settimeout(10)
# read each line from targets.txt
f = open("targets.txt", "r")
datalist = []
line = f.readline().rstrip()
# get my IP Address
me = socket.gethostbyname(socket.gethostname())
while line:
    print(line)
    host = socket.gethostbyname(line)
    startTime = datetime.now()
    senderSocket.sendto(payload, (host, TR_PORT))
    try:
        result = recv_sock.recv(1500)
        endTime = datetime.now()
        data = ext.getInfo(host, result, startTime, endTime)
    except socket.timeout:
        # whoops no response
        try:
            # resend packet
            startTime = datetime.now()
            senderSocket.sendto(payload, (host, TR_PORT))
            result = recv_sock.recv(1500)
            endTime = datetime.now()
            data = ext.getInfo(host, result, startTime, endTime)
        except socket.timeout:
            endTime = datetime.now()
            startTime = datetime.now()
            # whoops still no response, provide null value
            data = ('-1', '-1', '0', 'False', 'False')
    value = (line,) + data
    datalist.append(value)
    print(value)
    ext.writeTo(path, value)
    line = f.readline().rstrip()

# Thus, the output of your tool must
# include, for each destination
#   (a) the number of router hops between you and the destination,
#   (b) the RTT between you and the destination
#   (c) the number of probe/response matching criteria that matched for this destination (see explanation below)

# Deliverables:
#   1. Submit to canvas: A single zip file with
# (a) all programs (make sure they are well commented and include instructions how to run them – arguments etc. Under-documented programs will be penalized.);
# (b) Project report that includes all measurement results, graphs, correlation coefficients, and conclusions that you draw from your measurements.
#   2. Place your project into directory “<home-directory>/project2” in your VM. (You can use sftp to upload.) Then create a copy of that directory, “<home-directory>/project2grading”. We will be testing your work by going into the project2grading directory and issuing the commands “python3 distMeasurement.py”.
