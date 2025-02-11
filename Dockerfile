FROM python:3.13
LABEL authors="spud"

WORKDIR /uaf-bus-tracker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

ENV TZ="America/Anchorage"

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY database.py .
COPY initalizaton.py .
COPY main.py .

COPY export.py .
COPY graph.py .

CMD ["python3", "main.py"]