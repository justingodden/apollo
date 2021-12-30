FROM python:3.9-slim

COPY . /app/

WORKDIR /app

RUN  pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]