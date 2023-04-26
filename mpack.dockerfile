FROM python:3.11
RUN pip install msgpack
COPY serializable.py .
COPY testers/mpack_tester/mpackTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "mpack"]