FROM python:3.9-slim-buster

COPY ./requirements.txt /
RUN pip install --no-cache -r requirements.txt
RUN python -m spacy download en_core_web_lg
EXPOSE 5000

COPY / /
CMD ["python", "/app/api.py"]
