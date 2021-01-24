FROM python:3.8-slim

ARG AWS_KEY=${{secrets.AWS_KEY}}
ARG AWS_SECRET=${{secrets.AWS_SECRET}}
ARG SPACE_NAME=${{secrets.SPACE_NAME}}
ARG SPACE_ENDPOINT=${{secrets.SPACE_ENDPOINT}}
ARG SPACE_REGION=${{secrets.SPACE_REGION}}

WORKDIR /myapp

RUN apt-get update

RUN apt-get install -y gcc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /myapp

RUN chmod +x -R entrypoint