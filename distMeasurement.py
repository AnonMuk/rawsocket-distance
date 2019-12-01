import struct
import socket
from datetime import datetime
import auxiliary as ext

TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value

# raw datagram message creation
path = "./results.csv"
msg = "measurement for class project; please direct inquiries to student Zubair Mukhi (zxm132@case.edu) or Professor Michael Rabinovich (mxr136@case.edu)"
payload = bytes(msg + "a" * (1472 - len(msg)), "ascii")
udp = socket.getprotobyname('udp')
icmp = socket.getprotobyname('icmp')
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
senderSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
# using timeout instead of polling. Trying twice at 30 seconds.
recv_sock.settimeout(30)
f = open("targets.txt", "r")
datalist = []
line = f.readine()
me = socket.gethostbyname(socket.gethostname())
while line:
    host = socket.gethostbyname(line)
    startTime = datetime.datetime.now()
    senderSocket.sendto(payload, (host, TR_PORT))
    try:
        result = recv_sock.recv(1500)
        endTime = datetime.datetime.now()
        data = ext.getInfo(host, result, startTime, endTime)
    except socket.timeout:
        # whoops no response
        try:
            # resend packet
            startTime = datetime.datetime.now()
            senderSocket.sendto(payload, (host, TR_PORT))
            result = recv_sock.recv(1500)
            endTime = datetime.datetime.now()
            data = ext.getInfo(host, result, startTime, endTime)
        except socket.timeout:
            endTime = datetime.datetime.now()
            startTime = datetime.datetime.now()
            # whoops still no response
            result = (-1, -1, 0, False, False)
    datalist.append(result + ", " + line)
    print(line + ": " + result)
    ext.writeTo(path, result)
    line = f.readline()

# fundamental assumption: given that a request to a port throws back an error, by setting a time-to-live for the packet larger than the expected number of hops, we can derive the number of hops as (initial TTL - TTL at target)

# Thus, the output of your tool must
# include, for each destination
#   (a) the number of router hops between you and the destination,
#   (b) the RTT between you and the destination
#   (c) the number of probe/response matching criteria that matched for this destination (see explanation below)
#   (d) (if time) the number of bytes of the original datagram included in the ICMP error message

# You will need to create a datagram with custom values of some header fields for your probe. The easiest way to do it is to create a socket of type socket.SOCK_DGRAM and then use setsockopt() to change just the fields of your socket that you need to change. Then you can send it with socket.sendto() without going through the trouble of building the rest of the headers yourself.

# A few other useful functions:
#   a. To extract a field from a packet, you can use “struct” module, in particular struct.unpack function. Keep in mind that whenever you extract a multi-byte integer (e.g., port number) you need to make make sure the order in which the bytes appear in the packet (the most significant byte first) matches the order in which these integers are represented in the computer you happen to use. A portable way to handle this is to use so-called “network order” when extracting the bytes from the packet. E.g., if packet[x:x+1] represents the two-bytes port number in a packet, your can convert it to int by the following:
# port_from_packet = struct.unpack("!H", packet[x:x+2])[0]
# Here, the first argument “!H” speficies format of the packet fragment being extracted, in this case signifying that the two bytes from packet appear in the network order (“!”) and they represent an unsigned short (“H”).
#   b. However, when you need to extract only a single byte, you can just convert it to integer using ord(byte) function.
# You will need to think how you will match ICMP responses with the probes you are sending out. Note that your socket may receive unrelated packets since there is no port number to distinguish “your” packets from someone else’s (i.e., another process running on your host). In principle, there are several possibilities:
# Compare the IP of measurement target to the source IP of the ICMP response and consider this a match if and only if the target icmp response has a matching ip id. Declare match.
# Compare the port dest from the probe datagram with information from the ICMP payload. Declare match.

# From the output of your tool, produce a scatter graph to visualize the correlation (use any tool you want for this, e.g., Excel): have hops on X-axis, RTT on Y-axis, and for each remote host, place a dot with corresponding coordinates on the graph. This is a typical technique to visualize correlation. Note, as mentioned, you may not get responses from some of the servers. In order to produce a meaningful scatterplot, pick some other sites that were not included in your original list of ten. Keep probing until you have around ten. You can say in your report that you are substituting these sites because your original sites did not respond.
# Deliverables:
#   1. Submit to canvas: A single zip file with (a) all programs (make sure they are well commented and include instructions how to run them – arguments etc. Under-documented programs will be penalized.); (b) Project report that includes all measurement results, graphs, correlation coefficients, and conclusions that you draw from your measurements.
#   2. Place your project into directory “<home-directory>/project2” in your VM. (You can use sftp to upload.) Then create a copy of that directory, “<home-directory>/project2grading”. We will be testing your work by going into the project2grading directory and issuing the commands “python3 distMeasurement.py”.
# Tips:
# 1. The machines may take a long time to execute your “sudo” commands. To save time, the best thing to do is to start by executing a “sudo bash” command, which will get you a shell prompt as a root. Then you can just run any commands you want there as a root.
