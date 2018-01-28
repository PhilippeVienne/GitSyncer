FROM python:3.5

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
VOLUME /app/staticfiles
ENV DATABASE_URL postgres://postgresql:postgresql@db:5432/gitsyncer

RUN chmod +x bash/run-prod.sh
CMD /app/bash/run-prod.sh
