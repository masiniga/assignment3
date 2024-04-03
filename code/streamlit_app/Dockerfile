
FROM python:3.10.4-slim

WORKDIR /streamlit_app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit.py"]