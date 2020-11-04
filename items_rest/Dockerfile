FROM python:3.8.6

RUN apt-get update && apt-get install -y netcat

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
