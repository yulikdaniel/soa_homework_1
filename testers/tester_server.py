import sys
import os
import socket
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

    while True:
        data, addr = sock.recvfrom(1024)
        logging.info("Running tests")
        answer = f"Tests for {arg} format\n" + run_tests()
        sock.sendto(answer.encode(), addr)
        logging.info("Sent response")