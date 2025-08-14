FROM python:3.9-slim

WORKDIR .

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5003

CMD ["python3","main.py"]
