FROM python:3.11
RUN pip install protobuf grpcio grpcio-tools
COPY testers/proto_tester/stressformat.proto .
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. stressformat.proto
COPY serializable.py .
COPY testers/proto_tester/protoTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "proto"]