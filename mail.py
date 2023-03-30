import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from os import getenv, remove
from main_functions import zip_screeners
from traceback import print_exc

def send_email_report():
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
    body = "Screeners of the specified market, download the zip file or read in Google Sheets"
    message.attach(MIMEText(body, "plain"))

    # Zip the directory of market screeners
    zip_file = zip_screeners()
    
    filename = "screeners.zip"
    # Add attachment to email
    with open(zip_file, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=zip_file)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
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

    remove(zip_file)

    # End the SMTP session
    session.quit()
