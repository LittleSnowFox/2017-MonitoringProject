# Mount the ubuntu picture
FROM ubuntu:latest

# Installations
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get install -y nodejs
RUN apt-get upgrade -y
RUN apt-get install postgresql-client python3 python3-pip nginx libpq-dev -y
RUN apt-get install python3 python3-pip redis-tools -y
RUN pip3 install --upgrade pip

# Mount the folder "code"
ADD . /code

# Define the working folder
WORKDIR /code

RUN npm install
RUN pip3 install -r server/requirements.txt
# Dynamic way of installing the application setup.py
RUN pip3 install -e .

ENV LANG='C.UTF-8' LC_ALL='C.UTF-8'

# Move the index.html in the default folder of the files served by Nginx
RUN cp -Rs /code/client/* /var/www/html/

# Execute commands
CMD ["bash", "-c", " sleep 5; service nginx start ; sh /code/server/init.sh"]
