FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app 

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
RUN python manage.py migrate
CMD ["python","manage.py", "runserver","0.0.0.0:8000"]
