FROM python:3.11-bookworm
LABEL authors="ЭБИТ"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]