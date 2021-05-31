import smtplib
import ssl
import email

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


def send(dest, subj, msg, window, login_list):
    port = 465
    context = ssl.create_default_context()
    mittente = login_list[0]
    password = login_list[1]
    destinatario = dest.get()
    message = f"Subject: {subj.get()} \n{msg.get('1.0', 'end-1c')}"

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mittente, password)
        server.sendmail(mittente, destinatario, message)
    window.destroy()


def sendV2(dest, subj, msg, path, window, login_list):
    subject = subj.get()
    body = msg.get('1.0', 'end-1c')
    sender = login_list[0]
    receiver = dest.get()
    password = login_list[1]

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    temp = path.split("/")
    filename = temp[len(temp)-1]

    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(path, "rb").read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition",
                    f"attachment; filename= {filename}",)
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, text)
    window.destroy()
