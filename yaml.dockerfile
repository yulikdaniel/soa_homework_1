FROM python:3.11
RUN pip install pyyaml
COPY serializable.py .
COPY testers/yaml_tester/yamlTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "yaml"]