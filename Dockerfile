FROM python:3.13
LABEL authors="spud"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

ENV TZ="America/Anchorage"

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY database.py .
COPY initalizaton.py .
COPY export.py .
COPY main.py .

CMD ["python3", "main.py"]