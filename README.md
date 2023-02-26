# Email manager

The Email manager allows you to create email account on Fastmail and automatically check inbox folder for new mails with provided time interval. 

## Prerequisites

Docker, Docker Compose must be installed.
If not, please see:

[Docker](https://docs.docker.com/engine/install/) and
[Docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
for installation instructions.


## Installation

1. Clone the repo:
```sh
https://github.com/AlexandrZhydyk/Email_manager.git
```

## Usage
1. Add app configuration to your .env file in the root of your project:
```sh
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

4. Manually create [Fastmail app password](https://www.fastmail.help/hc/en-us/articles/360058752854) for access to your email by the script.
Please add, just generated password to already created file `email_accounts_data.json` under key `password`.
```sh
vim email_accounts_data.json
i - enter to insert mode to change value
Esc
:wq - to save the changes
```
5. Finally, the scripts will monitor email inbox folder each 5 minutes to reply.

  
6. To change checking interval edit `crontab` file:
```sh
docker compose exec mailing bash
cd ..
crontab -e
```
