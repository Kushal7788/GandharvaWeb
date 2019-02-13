import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(to_email, subject= None, message = None, attach = None,otp=0):
    # Define from
    sender = 'hello@viitgandharva.com'

    # Create message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    if otp==0:
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message))
    # Attach File
    for f in attach or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

    # Perform operations via server
    server.login('hello@viitgandharva.com', 'Gandharva@19hello')
    server.sendmail(sender, to_email, msg.as_string())
    server.quit()