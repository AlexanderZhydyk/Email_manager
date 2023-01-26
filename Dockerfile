FROM python:3.10

RUN apt update

RUN mkdir "checklab"

WORKDIR /checklab

COPY ./cron/crontab /etc/cron.d/crontab
COPY ./start.sh ./start.sh
COPY ./src ./src
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN python -m pip install --upgrade pip
RUN apt-get install -y cron
RUN pip install pipenv
RUN pipenv install --system --deploy

RUN touch /var/log/cron.log
RUN chmod +x ./start.sh
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["bash"]
