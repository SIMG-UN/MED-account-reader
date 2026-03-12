import yaml
import logging

def load_credentials(filepath):
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            user = credentials['user']
            password = credentials['password']
            return user, password
    except Exception as e:
        logging.error("Failed to load credentials: {}".format(e))
        raise


import imaplib
import email

def connect_to_gmail_imap(user, password):
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select('inbox')  # Conectarse al INBOX
        status, messages = mail.search(None, 'FROM "alertasynotificaciones@an.notificacionesbancolombia.com"')
        for num in messages[0].split()[-1:]:

            status, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            print(msg["From"])
            print(msg["Subject"])

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True)
                        if "Todo salió bien" in body.decode():
                            print(body.decode())
            else:
                print("Here!")
                body = msg.get_payload(decode=True)
                print(body.decode())
        return mail
    
    except Exception as e:
        logging.error("Connection failed: {}".format(e))
        raise

user, password = load_credentials("credentials.yaml")
print("User: ", user)

mail = connect_to_gmail_imap(user, password)