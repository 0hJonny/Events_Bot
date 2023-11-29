FROM python:3.11-alpine
LABEL authors="ЭБИТ"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "./bot.py" ]