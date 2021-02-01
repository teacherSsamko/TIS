FROM python:3.8.5

WORKDIR /health
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python ./app.py
