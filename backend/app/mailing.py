import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_user_confirmation_email(to_email, confirmation_token):
    YOUR_GOOGLE_EMAIL = 'recruiters788@gmail.com'
    YOUR_GOOGLE_EMAIL_APP_PASSWORD = 'uicl ojlm pinv hgzv'

    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)

    # Construct the email
    msg = MIMEMultipart()
    msg['From'] = YOUR_GOOGLE_EMAIL
    msg['To'] = to_email
    msg['Subject'] = 'Confirm Your Email Address'

    # Email body
    body = f'''
    Thank you for registering. Please click the following link to confirm your email address:
    http://127.0.0.1:8000/confirm_user_email?token={confirmation_token}
    '''
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    smtpserver.send_message(msg)

    # Close connection
    smtpserver.close()


def send_company_confirmation_email(to_email, confirmation_token):
    YOUR_GOOGLE_EMAIL = 'sandeshxandey0@gmail.com'
    YOUR_GOOGLE_EMAIL_APP_PASSWORD = 'wmof vicx oxyv xfzo'

    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)

    # Construct the email
    msg = MIMEMultipart()
    msg['From'] = YOUR_GOOGLE_EMAIL
    msg['To'] = to_email
    msg['Subject'] = 'Confirm Your Email Address'

    # Email body
    body = f'''
    Thank you for registering. Please click the following link to confirm your email address:
    http://127.0.0.1:8000/confirm_company_email?token={confirmation_token}
    '''
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    smtpserver.send_message(msg)

    # Close connection
    smtpserver.close()
