FROM tensorflow/tensorflow

COPY . /app/

WORKDIR /app

RUN  pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]