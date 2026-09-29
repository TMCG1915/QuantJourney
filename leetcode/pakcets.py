import math

packets = [12, 25, 10, 7, 8]


def maxPackets(packets: list) -> int:
    n = len(packets)
    max_packets = 0
    leftover = 0

    for i in range(n):
        k = math.floor(math.log(packets[i], 2))
        packets[i] += leftover
        leftover = packets[i] - 2**k
        max_packets = max(2**k, max_packets)

    return(max_packets)

print(maxPackets(packets))
                       