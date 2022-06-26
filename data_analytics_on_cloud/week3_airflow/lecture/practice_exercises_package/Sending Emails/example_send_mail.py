# Import libraries to send email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Set variables
sender = ''
receiver = ''
subject = ''
body = ''
file_path = ''

# Create an instance of MIMEMultipart
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))
    
if file_path:
    # Open file to be attached
    attachment = open(file_path, "rb")
    # Prepare attachment and add to the message
    att = MIMEBase('application', 'octet-stream')
    att.set_payload((attachment).read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', f"attachment; filename= {file_path}")
    msg.attach(att)

# Create SMTP session and send the mail
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls() # to create a secure channel
s.login('', '') # add email and password and login
text = msg.as_string()
s.sendmail(sender, receiver, text)
# Terminate the session
s.quit()