FROM python:3.8
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/GlobalRedPyme
EXPOSE 8001
RUN python manage.py crontab add
RUN service cron restart
CMD python manage.py runserver 0.0.0.0:8001

