# we want to go from the base image of python:3.7
FROM python:3.7

# this is the equivalent of us "cd /app" from
# our within the container after we start it
WORKDIR /app

# let's copy requirements.txt into /app
COPY requirements.txt .

# let's copy src folder into /app
COPY src src

# install dependencies
RUN pip install -r requirements.txt

# this will run when we run our
# docker container
ENTRYPOINT ["python", "src/main.py"]