import smtplib
import imaplib

gmail_user = 'gregshneck@gmail.com'
gmail_pass = 'GregShneck_1'

# -- Log in --
server_smtp = smtplib.SMTP('smtp.gmail.com', 587) #465 SSL
server_smtp.starttls()
print(server_smtp.login(gmail_user, gmail_pass))
server_imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
print(server_imap.login(gmail_user, gmail_pass))


print(server_imap.select('INBOX'))
# -- Get number of unread messages --
server_imap.select('INBOX')
print('No.of unread messages: ' + str(len(server_imap.search(None, 'UNSEEN')[1][0].split())))


# -- Get last N received messages (display subject, date, sender), ordered by date --
typ, data = server_imap.search(None, 'SEEN')
for num in data[0].split():
    typ, data = server_imap.fetch(num, '(RFC822)')
    print('Message %s\n%s\n' % (num, data[0][1]))
    message = data[0][1].lstrip('Subject: ').strip() + ' '
    print(message)

# -- Send a message. Next fields must be available - subject, recipient, CC, body --
receivers = ['ana_shutreac@yahoo.com', 'ana.shutreac@gmail.com']

message = """From: Greg Shneck <gregshneck@gmail.com>
To: Ana Shutreac <ana_shutreac@yahoo.com>
Cc: Ana Shutreac <ana.shutreac@gmail.com>
Subject: SMTP Test

This is a test e-mail message.
"""
try:
    server_smtp.sendmail(gmail_user, receivers, message)
    print('Success')
except:
    print('Error')














