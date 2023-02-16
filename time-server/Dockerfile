FROM python:3.10-slim

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]

