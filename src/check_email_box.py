import json
import os
import email
import email.utils
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from gpt3_chatbot import get_reply


IMAP_SERVER = 'imap.fastmail.com'
IMAP_PORT = 993
SMTP_SERVER = 'smtp.fastmail.com'
SMTP_PORT = 587


def get_smtp_server(user_email, password):
    try:
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(user_email, password)
        return smtp
    except smtplib.SMTPAuthenticationError as err:
        print(f"SMTP login failed! Error: {err}")
    except Exception as err:
        print(f"SMTP connection/login failed! Error: {err}")


def get_imap_server(user_email, password):
    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(user_email, password)
        return imap
    except imaplib.IMAP4_SSL.error as err:
        print(f"IMAP login failed! Error: {err}")
    except Exception as err:
        print(f"IMAP connection/login failed! Error: {err}")


def send_message(smtp_server, message):
    try:
        reply_email = MIMEMultipart()
        reply_email['From'] = message.get("To")
        reply_email['To'] = message.get("From")
        reply_email['Subject'] = f'Re: {message.get("Subject")}'
        reply_email['References'] = message.get("Message-Id")
        received_mail_body = ""
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                received_mail_body = part.get_payload(decode=True)

        gpt_reply = get_reply(received_mail_body.decode())

        reply_email.attach(MIMEText(gpt_reply, 'plain'))
        text = reply_email.as_string()
        smtp_server.sendmail(reply_email['From'], reply_email['To'], text)
        return True
    except Exception as err:
        print(err)
        return False


def get_unseen_messages(imap_server):
    messages = []
    try:
        imap_server.select('Inbox')
        _, msg_nums = imap_server.search(None, "UNSEEN")
        for msg_num in msg_nums[0].split():
            _, data = imap_server.fetch(msg_num, "(RFC822)")
            messages.append((msg_num, email.message_from_bytes(data[0][1])))
        return messages
    except Exception as err:
        print(err)


def reply_to_messages(messages, smtp_server, imap_server):
    try:
        for msg_num, message in messages:
            message_status = send_message(smtp_server, message)
            if message_status:
                imap_server.store(msg_num, '+FLAGS', '\\Seen')
    except Exception as err:
        print(err)


def main():
    # Extract user data from the file
    with open('email_accounts_data.json', 'r') as file:
        user_data = json.loads(file.read())
        user_email = user_data.get('email')
        password = user_data.get('password')

    if user_email and password:
        smtp_server = get_smtp_server(user_email, password)
        imap_server = get_imap_server(user_email, password)
        messages = get_unseen_messages(imap_server)
        reply_to_messages(messages, smtp_server, imap_server)
        smtp_server.quit()
        imap_server.close()


if __name__ == '__main__':
    main()
