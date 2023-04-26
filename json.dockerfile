FROM python:3.11
COPY serializable.py .
COPY testers/json_tester/jsonTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "JSON"]