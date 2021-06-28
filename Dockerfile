FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip3 install -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations 
RUN python manage.py migrate
EXPOSE 8000
CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]