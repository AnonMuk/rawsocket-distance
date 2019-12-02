import struct


TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value


def getInfo(host, result, startTime, endTime):
    matchNum = 0
    totalTime = (endTime - startTime).total_seconds() * 1000  # to msec
    hops = TTL - result[8]
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
    #  44-48
    target_ip = ("{}.{}.{}.{}".format(result[12], result[13], result[14], result[15]))
    return (target_ip == host)


def Case2(result):
    return (struct.unpack("!H", result[50:52])[0] == TR_PORT)


def writeTo(path, msg):
    f = open(path, "a+")
    f.write(convertTuple(msg) + "\n")
    f.close()


def convertTuple(tuple):
    commaString = ",".join(tuple)
    return commaString
