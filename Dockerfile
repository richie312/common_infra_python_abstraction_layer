FROM python:3.9-slim

WORKDIR .

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY startup.sh /usr/local/bin/startup.sh # Copy the startup script
RUN chmod +x /usr/local/bin/startup.sh # Make it executable

EXPOSE 5003

# Use ENTRYPOINT to run the startup script, which in turn executes your main application.
ENTRYPOINT ["/usr/local/bin/startup.sh"]
CMD ["python3","main.py"]