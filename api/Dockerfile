# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]