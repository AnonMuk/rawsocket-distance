import struct


TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value


def getInfo(host, port, result, startTime, endTime):
    matchNum = 0
    totalTime = (endTime - startTime).total_seconds()
    hops = TTL - result[8]
    if (hops < 0):
        hops = -1
    a = Case1(result, host)
    b = Case2(result, port)
    if(a):
        matchNum += 1
    if (b):
        matchNum += 1
    return (str(hops), str(totalTime), str(matchNum), str(a), str(b))


def Case1(result, host):
    #  44-48
    target_ip = ("{}.{}.{}.{}".format(result[44], result[45], result[46], result[47]))
    return (target_ip == host)


def Case2(result, port):
    return (struct.unpack("!H", result[23:25])[0] == port)


def writeTo(path, msg):
    f = open(path, "a+")
    f.write(convertTuple(msg))
    f.close()


def convertTuple(tuple):
    commaString = ",".join(tuple)
    return commaString
