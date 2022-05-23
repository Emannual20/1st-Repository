import smtplib
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#mailFrom = "nftolympus2022@gmail.com"
#mailTo = "gamerism202@gmail.com"
#msg = MIMEMultipart('alternative')
#msg['Subject'] = "Change of password"
#msg['From'] = mailFrom
#msg['To'] = mailTo
#emailBody = 'sup'

#msg.attach(MIMEText(emailBody, "html"))

#mail = smtplib.SMTP('smtp.gmail.com', 587)
#mail.ehlo
#mail.starttls()
#mail.login('nftolympus2022@gmail.com', 'NewUser2022')
#mail.sendmail(mailFrom, mailTo, msg.as_string())
#mail.quit()

def send_email_gmail(subject, message, destination):
    # First assemble the message
    msg = MIMEText(message, 'plain')
    msg['Subject'] = subject

    # Login and send the message
    port = 465
    my_mail = 'nftolympus2022@gmail.com'
    my_password = 'NewUser2022'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(my_mail, my_password)
        server.sendmail(my_mail, destination, msg.as_string())


send_email_gmail('nftolympus2022@gmail.com', 'This is the message', 'gamerism202@gmail.com')
