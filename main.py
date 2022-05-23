import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create email to send new password
mailFrom = "nftolympus2022@gmail.com"
mailTo = "gamerism202@gmail.com"
msg = MIMEMultipart('alternative')
msg['Subject'] = "Change of password"
msg['From'] = mailFrom
msg['To'] = mailTo
emailBody = 'sup'

msg.attach(MIMEText(emailBody, "html"))

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo
mail.starttls()
mail.login('nftolympus2022@gmail.com', 'NewUser2022')
mail.sendmail(mailFrom, mailTo, msg.as_string())
mail.quit()