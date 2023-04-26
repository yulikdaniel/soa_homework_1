FROM python:3.11
RUN pip install avro
COPY serializable.py .
COPY testers/avro_tester/avroTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "avro"]