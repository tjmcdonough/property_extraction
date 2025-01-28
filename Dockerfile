FROM python:3.13-slim
WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade -r requirements.txt

EXPOSE 8080

COPY ./ /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]