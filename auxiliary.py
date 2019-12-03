import struct


TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value


def getInfo(host, result, startTime, endTime):
    # create a constant to track the number of matching criteria as below
    matchNum = 0
    totalTime = (endTime - startTime).total_seconds() * 1000  # time delta in seconds to msec
    hops = TTL - result[36]  # extract TTL field from ICMP packet (not from response header whoops)
    if (hops < 0):
        hops = -1
    a = Case1(result, host)
    b = Case2(result)
    if(a):
        matchNum += 1
    if (b):
        matchNum += 1
    return (str(hops), str(totalTime), str(matchNum), str(a), str(b))


def Case1(result, host):
    # pull IP address out of packet, match it to socket.gethostbyname
    target_ip = ("{}.{}.{}.{}".format(result[12], result[13], result[14], result[15]))
    return (target_ip == host)


def Case2(result):
    # match port from ICMP returned packet to traceroute port
    return (struct.unpack("!H", result[50:52])[0] == TR_PORT)


def writeTo(path, msg):
    f = open(path, "a+")
    f.write(convertTuple(msg) + "\n")
    f.close()


def convertTuple(tuple):
    commaString = ",".join(tuple)
    return commaString
