FROM python:3.10-slim

COPY . .

RUN pip3 install -r requirements.txt

CMD uvicorn app:api --port 8050 --reload 

EXPOSE 8050