FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

COPY /entrypoint.prod.sh /entrypoint.prod.sh
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:7070", "foodgram.wsgi"]