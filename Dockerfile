FROM python:3.11.6-bullseye

RUN apt update
RUN apt -yV upgrade
# TimeZone
RUN apt -y install tzdata && \
cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN pip install -U pip==23.3.1
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/. .
COPY .env .

CMD ["python", "main.py"]
