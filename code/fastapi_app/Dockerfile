FROM python:3.10.4-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /fastapi_app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]

