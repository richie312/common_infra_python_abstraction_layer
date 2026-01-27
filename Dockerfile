FROM python:3.9-slim
RUN apt-get update && apt-get install -y cron curl
WORKDIR .
COPY . .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5003
RUN chmod +x startup.sh
CMD ["python3","main.py"]