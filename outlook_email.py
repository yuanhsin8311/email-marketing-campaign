import smtplib
import string, random
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sender_email_address = 'cinyuan@outlook.com'
sender_email_password = 'Saga11831'
#receiver_email_address = 'yhuang7211@gmail.com;yuanhsin8311@gmail.com'
receiver_email_address_list = ['yhuang7211@gmail.com', 'yuanhsin8311@gmail.com']
#receiver_email_address = ''
email_subject_line = 'Python Email Campaign Demo'

server = smtplib.SMTP('smtp-mail.outlook.com:587')
server.starttls()
server.login(sender_email_address, sender_email_password)

for receiver_email_address in receiver_email_address_list:
    random_account_name = ''.join(random.choice(string.ascii_letters) for x in range(10))
    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Hello VIP\n' + 'http://127.0.0.1:5000/lookup.html?Name=' + random_account_name

    msg.attach(MIMEText(email_body, 'plain'))

    email_content = msg.as_string()
    print (email_content)

    server.sendmail(sender_email_address, receiver_email_address, email_content)
    time.sleep(10)

server.quit()
