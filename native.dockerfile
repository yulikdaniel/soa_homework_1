FROM python:3.11
COPY serializable.py .
COPY testers/native_tester/nativeTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "native"]