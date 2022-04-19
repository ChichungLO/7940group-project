FROM python:latest
COPY chatbot.py /
COPY requirements.txt /
COPY config.ini /
CMD ["chatbot.py"]
ENTRYPOINT ["python"]