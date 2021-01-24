FROM python:3.8-slim

WORKDIR /myapp

RUN apt-get update

RUN apt-get install -y gcc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /myapp

RUN chmod +x -R entrypoint