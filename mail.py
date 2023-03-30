import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from os import getenv
from main_functions import get_files
from traceback import print_exc

def send_email_report(market):
    # Set the email addresses and password
    load_dotenv()
    sender_email = getenv("sender_email")
    receiver_email = getenv("receiver_email")
    email_password = getenv("email_password")
    sender_email_address = f"{sender_email}"
    receiver_email_address = f"{receiver_email}"
    password = f"{email_password}"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email_address
    message["To"] = receiver_email_address
    message["Subject"] = "Daily Finance Report"

    # Add body to email
    body = "Report for all the markets you asked."
    message.attach(MIMEText(body, "plain"))

    # Retrieve the files we want to send
    files = get_files(market)
    
    # Add attachment to email
    for file in files:
        with open(file, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=file)
            part['Content-Disposition'] = f'attachment; filename="{file}"'
            message.attach(part)

    # Create SMTP session for sending the email
    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_email_address, password)

    # Send the email
    try:
        text = message.as_string()
        session.sendmail(sender_email_address, receiver_email_address, text)
        print("Email sent")
    except:
        print_exc()

    # End the SMTP session
    session.quit()
