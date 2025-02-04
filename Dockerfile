FROM python:3.13
LABEL authors="spud"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]