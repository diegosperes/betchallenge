from python:3.7.2-alpine3.8

ENV ENV=prod

COPY ./requirements.txt /app/
COPY ./Makefile /app/
WORKDIR /app

RUN apk add build-base \
	&& echo `python --version` \
	&& pip install -U setuptools pip \
	&& make setup

COPY ./betbright /app/betbright/

EXPOSE 8000

CMD ["make", "run-worker"]
CMD ["make", "run-server"]
