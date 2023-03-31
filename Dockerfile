FROM python:3.8.10-slim
WORKDIR /app

RUN apt update && apt install ffmpeg -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt \
    && rm requirements.txt \
    && rm -r /root/.cache/pip

COPY . .
ENV ROOT_DIR /app/src/
CMD [ "python3", "./src/main.py"]
