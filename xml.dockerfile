FROM python:3.11
RUN pip install xmltodict
COPY serializable.py .
COPY testers/xml_tester/xmlTester.py .
COPY testers/tester_server.py .
CMD ["python3", "tester_server.py", "XML"]