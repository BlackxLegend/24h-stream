FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt

EXPOSE 80

CMD ["python", "stream.py"]
