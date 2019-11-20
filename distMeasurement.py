import struct
import socket

TR_PORT = 33434 # Port 33434 is a traceroute port
MAX_TTL = 255 # Max time to live is 255, I think
TTL = 64 # standard time to live value

# raw datagram message creation
msg = "measurement for class project; please direct inquiries to student Zubair Mukhi (zxm132@case.edu) or Professor Michael Rabinovich (mxr136@case.edu)"
payload = bytes(msg + "a"*(1472-len(msg)), "ascii")
udp = socket.getprotobyname('udp')
icmp = socket.getprotobyname('icmp')
senderSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, udp)
senderSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
#using timeout instead of polling. Trying twice at 30 seconds.
recv_sock.settimeout(30)
f = open("targets.txt", "r")
datalist = []
line = f.readine()
while line:
    host = socket.gethostbyname(line)
    senderSocket.sendto(payload, (host, TR_PORT))
    try:
        result = recv_sock.recv(1500)
    except timeout:
        #whoops no response
        try:
            #resend packet
            senderSocket.sendto(payload, (host, TR_PORT))
            result = recv_sock.recv(1500)
        except timeout:
            #whoops still no response
            result = "error on " + line
    datalist.append(result)
    line = f.readline()


# fundamental assumption: given that a request to a port throws back an error, by setting a time-to-live for the packet larger than the expected number of hops, we can derive the number of hops as (initial TTL - TTL at target)

# use raw sockets in order to send and receive completely custom packets

# Thus, the output of your tool must
# include, for each destination
#   (a) the number of router hops between you and the destination,
#   (b) the RTT between you and the destination
#   (c) the number of probe/response matching criteria that matched for this destination (see explanation below)
#   (d) the number of bytes of the original datagram included in the ICMP error message

# You will need to create a datagram with custom values of some header fields for your probe. The easiest way to do it is to create a socket of type socket.SOCK_DGRAM and then use setsockopt() to change just the fields of your socket that you need to change. Then you can send it with socket.sendto() without going through the trouble of building the rest of the headers yourself.

# You will also need to create a raw socket to receive ICMP messages. To create a raw socket for receiving an ICMP datagram, you can use the following function:
# recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
# after which you can get a packet from this socket by using the following:
# icmp_packet = recv_sock.recv(max_length_of_expected_packet)

# A few other useful functions:
#   a. To extract a field from a packet, you can use “struct” module, in particular struct.unpack function. Keep in mind that whenever you extract a multi-byte integer (e.g., port number) you need to make make sure the order in which the bytes appear in the packet (the most significant byte first) matches the order in which these integers are represented in the computer you happen to use. A portable way to handle this is to use so-called “network order” when extracting the bytes from the packet. E.g., if packet[x:x+1] represents the two-bytes port number in a packet, your can convert it to int by the following:
# port_from_packet = struct.unpack("!H", packet[x:x+2])[0]
# Here, the first argument “!H” speficies format of the packet fragment being extracted, in this case signifying that the two bytes from packet appear in the network order (“!”) and they represent an unsigned short (“H”).
#   b. However, when you need to extract only a single byte, you can just convert it to integer using ord(byte) function.
# You will need to think how you will match ICMP responses with the probes you are sending out. Note that your socket may receive unrelated packets since there is no port number to distinguish “your” packets from someone else’s (i.e., another process running on your host). In principle, there are several possibilities: one technique would compare the IP address of your measurement target to the source IP address of the ICMP response and match probes with ICMP responses when these IP addresses match. This technique is going to work most of the time but not all the time: sometime you may receive the ICMP response from an IP address that is different from the address you are probing. (We have actually seen this behavior. I speculate it’s due to the use of a load balancer at the destination. In this setup, when you resolve the destination’s hostname, you get the IP address of the load balancer, which receives your packets and forwards them to one of the servers in a server cluster. However, the ICMP messages that the selected server generates, carry the server’s own IP address, which is different from that of the load balance which your probe used.) Another technique matches the datagram ID (the “IPID” field from the IP header) with the datagram ID you find in the ICMP payload (which, as a reminder, contains full IP header plus 8 bytes of the transport-level header of the original datagram in those first 28 bytes of payload). Again, this will work most of the time but does not guarantee to work all the time because a NAT box, a firewall, or another middlebox between you and the destination may change the IPID of the datagram as it forwards it along. Yet another technique involves matching the destination port number from your probe datagram with the corresponding information from the 28-byte ICMP payload. This is unlikely to be changed by any middlebox. Thus, I would like you to implement all three techniques above and declare a match when any of the three techniques produce a match. For each destination, please report how many of the three techniques above produced a match.
# You need to allow for a possibility that you will get no answer – because the target host does not send ICMP error messages, or because the destination’s firewall blocks outgoing ICMP messages, or because the destination’s firewall blocks unexpected UDP messages. Hence your program should not be stuck on reading from a socket forever. You will need to use either a “select” or “poll” call on the socket (read about them – google for “socket select”) before reading from the socket. WARNING: do not process this error by changing the destination port number – stick with 33434 or you may get a nasty call from network admins! This will be interpreted as port scanning. I suggest you just try couple times and if you still get no answer, give up on this destination and produce some error message and move on to measuring the next site. You can check manually if it is your program’s fault by trying to reach this destination using a standard ping measurement (there is a small chance that ping would be treated differently and experience a different outcome, but if you see that your tool produces no answer while ping succeeds on many destinations, this should increase your doubt in the correctness of your tool).
# (8) While in theory you can address your probe to any unreachable port, how would you know which port on the target host is unused by other applications? There is a specially allocated port number for this type of probing by traceroute, and please use that port number, which is 33434. Your script should read the file “targets.txt” (collocated in the same directory as your script), which includes the set of websites you are exploring and accept no arguments, and obtain the IP address of each target using socket.gethostbyname method. The script should print out the result on standard output (in addition to any file that you find convenient to produce the plot below) that is understandable to the grader. Please name the script “distMeasurement.py”. Once you have your tool, measure the hop count as well as RTT to each of the websites you worked with in earlier homework assignments (or read instructions for the eecs425 portion of HW 2 if you are a 325 student). From the output of your tool, produce a scatter graph to visualize the correlation (use any tool you want for this, e.g., Excel): have hops on X-axis, RTT on Y-axis, and for each remote host, place a dot with corresponding coordinates on the graph. This is a typical technique to visualize correlation. Note, as mentioned, you may not get responses from some of the servers. In order to produce a meaningful scatterplot, pick some other sites that were not included in your original list of ten. Keep probing until you have around ten. You can say in your report that you are substituting these sites because your original sites did not respond.
# Deliverables:
#   1. Submit to canvas: A single zip file with (a) all programs (make sure they are well commented and include instructions how to run them – arguments etc. Under-documented programs will be penalized.); (b) Project report that includes all measurement results, graphs, correlation coefficients, and conclusions that you draw from your measurements.
#   2. Place your project into directory “<home-directory>/project2” in your VM. (You can use sftp to upload.) Then create a copy of that directory, “<home-directory>/project2grading”. We will be testing your work by going into the project2grading directory and issuing the commands “python3 distMeasurement.py”.
# Tips:
# 1. The machines may take a long time to execute your “sudo” commands. To save time, the best thing to do is to start by executing a “sudo bash” command, which will get you a shell prompt as a root. Then you can just run any commands you want there as a root.
