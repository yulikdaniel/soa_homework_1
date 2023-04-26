import socket
import os
import logging

logging.basicConfig(level=logging.INFO)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", int(os.getenv("PROXY_PORT"))))

logging.info(f'Started listening on {("0.0.0.0", int(os.getenv("PROXY_PORT")))}')

while True:
    tester, query_author = sock.recvfrom(1024)
    tester = tester.decode()
    logging.info(f"Received {tester} from {query_author}")
    if tester == "ALL":
        for tester in os.getenv("BROADCAST_LIST", "NATIVE").split(","):
            logging.info(f'Sending message to {(os.getenv(tester + "_HOST"), int(os.getenv(tester + "_PORT")))}')
            sock.sendto(b"RUN", (os.getenv(tester + "_HOST"), int(os.getenv(tester + "_PORT"))))
            data, addr = sock.recvfrom(1024)
            logging.info("Redirecting response")
            sock.sendto(data, query_author)
    else:
        logging.info(f'Sending message to {(os.getenv(tester + "_HOST"), int(os.getenv(tester + "_PORT")))}')
        sock.sendto(b"RUN", (os.getenv(tester + "_HOST"), int(os.getenv(tester + "_PORT"))))
        data, addr = sock.recvfrom(1024)
        logging.info("Redirecting response")
        sock.sendto(data, query_author)
