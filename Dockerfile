FROM python:slim
ENV TELEGRAM_API_TOKEN="${TELEGRAM_API_TOKEN}"
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY *.py ./
CMD ["python3", "main.py"]