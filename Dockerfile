#Use Python 3.11 as the base image

FROM python:3.11-slim

#Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container

COPY . /app
#Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy the Python scripts and other necessary files



#Create a directory for data

EXPOSE 80

#Set the environment variable for Python to run in unbuffered mode ENV PYTHONUNBUFFERED-1

#Command to run the script

CMD ["python", "agents.py"]