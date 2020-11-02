FROM python:3

COPY . /views
WORKDIR /views

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["views.py"]