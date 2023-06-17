# init a base image
FROM python:3.9-slim-buster
# update pip
RUN pip3 install --upgrade pip
# define the working directory
WORKDIR /usr/app/data
# copy requirements.txt
COPY requirements.txt requirements.txt
# run pip to install flask dependency
RUN pip3 install -r requirements.txt
# copy the contents into the working directory
COPY . .
# expose port
EXPOSE 6000
ENV FLASK_APP=app1.py
# define the command to execute the flask app
CMD ["python3", "-m", "flask", "run" ,"--host=0.0.0.0", "--port=6000"]
