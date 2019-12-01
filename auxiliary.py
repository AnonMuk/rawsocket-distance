TR_PORT = 33434  # Port 33434 is a traceroute port
TTL = 64  # standard time to live value


def getInfo(result, startTime, endTime):
    totalTime = (endTime - startTime).total_seconds()
    target_ip = (result[12], result[13], result[14], result[15])
    src_ip = (result[15], result[16], result[17], result[18])
    hops = TTL - result[8]
    if (hops < 0):
        hops = -1
    return (hops, totalTime, Case1(result), Case2(result))


def Case1(result):
    stub = True
    # Stub logic here
    return stub


def Case2(result):
    stub = True
    # Stub logic here
    return stub


def writeTo(path, msg):
    f = open(path, "a+")
    f.write(msg)
    f.close()
