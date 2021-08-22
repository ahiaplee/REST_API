
FROM python:3.6.9
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
#RUN pip install redis

# copy project
COPY . /usr/src/app/

EXPOSE 5000
EXPOSE 5432

#RUN ls -la app/
