FROM python:3.12

COPY src/ .
COPY requirements.txt .
COPY run_docker.sh .

RUN pip3 install -r requirements.txt

CMD ["./run_docker.sh"]

