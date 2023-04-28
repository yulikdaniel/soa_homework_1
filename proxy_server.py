import socket
import os
import logging
import struct

logging.basicConfig(level=logging.INFO)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
sock.bind(("0.0.0.0", int(os.getenv("PROXY_PORT"))))

logging.info(f'Started listening on {("0.0.0.0", int(os.getenv("PROXY_PORT")))}')

while True:
    tester, query_author = sock.recvfrom(1024)
    tester = tester.decode().strip()
    logging.info(f"Received {tester} from {query_author}")
    if tester == "ALL":
        logging.info(f'Sending message to {(os.getenv("MULTICAST_HOST"), int(os.getenv("MULTICAST_PORT")))}')
        sock.sendto(b"RUN", (os.getenv("MULTICAST_HOST"), int(os.getenv("MULTICAST_PORT"))))
        for _ in range(int(os.getenv("NUM_TESTERS", 7))):
            data, addr = sock.recvfrom(1024)
            logging.info("Redirecting response")
            sock.sendto(data, query_author)
    else:
        logging.info(f'Sending message to {(os.getenv(tester + "_HOST"), int(os.getenv(tester + "_PORT")))}')
        sock.sendto(b"RUN", (os.getenv(tester + "_HOST"), int(os.getenv(tester + "_PORT"))))
        data, addr = sock.recvfrom(1024)
        logging.info("Redirecting response")
        sock.sendto(data, query_author)
