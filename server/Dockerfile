FROM python:3.7-slim
RUN apt-get update
# libpq-dev gcc are added here to ensure psychopg2 installs correctly
RUN apt-get install -y git python3-pip python3-dev libpq-dev gcc
COPY requirements.txt /server/requirements.txt

WORKDIR /server
RUN pip3 install -r requirements.txt

# remove gcc when done with installing psycopg2
RUN apt-get autoremove -y gcc
COPY . /server
ENTRYPOINT ["python", "run.py"]
