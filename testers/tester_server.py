import sys
import os
import socket
import struct
import logging

if __name__ == "__main__":
    arg = sys.argv[1]

    logging.basicConfig(level=logging.INFO)

    match arg:
        case "native":
            from nativeTester import run_tests
        case "JSON":
            from jsonTester import run_tests
        case "XML":
            from xmlTester import run_tests
        case "proto":
            from protoTester import run_tests
        case "avro":
            from avroTester import run_tests
        case "yaml":
            from yamlTester import run_tests
        case "mpack":
            from mpackTester import run_tests

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", int(os.getenv("PORT", "2001"))))
    logging.info(f'Started listening on {("0.0.0.0", int(os.getenv("PORT", "2001")))}')

    logging.info(f'Registered for multicast on host {os.getenv("MULTICAST_HOST", "224.3.29.71")}')
    group = socket.inet_aton(os.getenv("MULTICAST_HOST", "224.3.29.71"))
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, addr = sock.recvfrom(1024)
        logging.info("Running tests")
        answer = f"Tests for {arg} format\n" + run_tests()
        sock.sendto(answer.encode(), addr)
        logging.info("Sent response")