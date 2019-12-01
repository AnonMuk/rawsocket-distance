TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value


def getInfo(host, result, startTime, endTime):
    matchNum = 0
    totalTime = (endTime - startTime).total_seconds()
    hops = TTL - result[8]
    if (hops < 0):
        hops = -1
    a = Case1(result, host)
    b = Case2(result)
    if(a):
        matchNum += 1
    if (b):
        matchNum += 1
    return (hops, totalTime, matchNum, a, b)


def Case1(result, host):
    #  44-48
    target_ip = ("{}.{}.{}.{}".format(result[44], result[45], result[46], result[47]))
    return (target_ip == host)


def Case2(result):
    stub = True
    # Stub logic here
    return stub


def writeTo(path, msg):
    f = open(path, "a+")
    f.write(msg)
    f.close()
