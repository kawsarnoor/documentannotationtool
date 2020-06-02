# Build backend
FROM python:3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt

COPY . . 

RUN ["apt-get", "install", "-y", "vim"]

CMD ["python", "app.py"]
