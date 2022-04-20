FROM python:latest
COPY chatbot.py /
COPY requirements.txt /
COPY config.ini /
RUN pip install pip update && pip install -r requirements.txt
CMD ["chatbot.py"]
ENTRYPOINT ["python"]