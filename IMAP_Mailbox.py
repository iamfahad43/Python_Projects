
MAIL_SERVER = 'imap.googlemail.com'
USERNAME = ''
PASSWORD = ''
MAILBOX = 'Inbox'
MAX_DAYS = 7 # Deletes messages older than a week
imap_host = 'gmail.com'

import imaplib
import datetime

today = datetime.date.today()
cutoff_date = today - datetime.timedelta(days=MAX_DAYS)
before_date = cutoff_date.strftime('%d-%b-%Y')

search_args = '(BEFORE "%s")' % before_date

imap = imaplib.IMAP4(MAIL_SERVER)

"""# connect to host using SSL
imap = imaplib.IMAP4_SSL(imap_host)"""
print("Before Login \n")
imap.login(USERNAME, PASSWORD)
imap.select(MAILBOX)

print("After Login \n")

typ, data = imap.search(None, 'ALL', search_args)
# typ, data = imap.search(None, 'ALL')

for num in data[0].split():
    imap.store(num, '+FLAGS', '\\Deleted')
    print("I'm reading \n")

imap.expunge()

imap.close()
imap.logout()



"""
import imaplib
import pprint

imap_host = 'imap.gmail.com'
imap_user = ''
imap_pass = ''

# connect to host using SSL
imap = imaplib.IMAP4_SSL(imap_host)

## login to server
imap.login(imap_user, imap_pass)

imap.select('Inbox')

tmp, data = imap.search(None, 'ALL')
for num in data[0].split():
	tmp, data = imap.fetch(num, '(RFC822)')
	print('Message: {0}\n'.format(num))
	pprint.pprint(data[0][1])
	break
imap.close()

"""