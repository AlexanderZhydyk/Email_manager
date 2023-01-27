# Email manager

The Email manager allows you to create email account and automatically checking it with provided time interval. 

## Prerequisites

Docker, Docker Compose must be installed.
If not, please see:

[Docker](https://docs.docker.com/engine/install/) and
[Docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
for installation instructions.


## Installation

1. Clone the repo:
```sh
git clone https://github.com/AlexandrZhydyk/checklab_task.git
```

## Usage
1. Add app configuration to your .env file in the root of your project:
```sh
IMAP_SERVER=YOUR_IMAP_SERVER
IMAP_PORT=YOUR_IMAP_PORT
SMTP_SERVER=YOUR_SMTP_SERVER
SMTP_PORT=YOUR_SMTP_PORT
OPENAI_KEY=YOUR_OPENAI_KEY
```

2. Run the command for building and running the images:
```sh
docker compose up -d --build
```

3. To create email account run the command:
```sh
docker compose exec mailing bash
cd src
python create_fastmail_account.py
```
> *Follow tips in the terminal.*


4. After email account be created, the scripts will monitor email inbox folder each 5 minutes to reply.

  
5. To change checking interval edit `cron/crontab` file:
```sh
docker compose exec mailing bash
cd ..
crontab -e
```
