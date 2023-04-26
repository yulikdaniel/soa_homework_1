FROM python:3.11
COPY proxy_server.py .
CMD ["python3", "proxy_server.py"]