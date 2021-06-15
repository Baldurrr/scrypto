# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
ADD requirements.txt requirements.txt 
ADD scrypto.py scrypto.py

# install dependencies
RUN pip3 install -r requirements.txt

# command to run on container start
CMD [ "python","-u","scrypto.py" ]
