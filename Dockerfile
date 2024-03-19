FROM python:3.9.17-slim-buster
# build variables.
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && apt-get update

# Install app dependencies
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# clean the install.
RUN apt-get -y clean
# copy all files to /app directory and move into directory.

# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]