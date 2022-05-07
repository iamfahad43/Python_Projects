MAIL_SERVER = ''
imap_user = ''
imap_pass = ''
MAILBOX = ''
MAX_DAYS = 7 # Deletes messages older than a week

import imaplib
import datetime

today = datetime.date.today()
cutoff_date = today - datetime.timedelta(days=MAX_DAYS)
before_date = cutoff_date.strftime('%d-%b-%Y')

search_args = '(BEFORE "%s")' % before_date

imap = imaplib.IMAP4_SSL(MAIL_SERVER)
imap.login(imap_user, imap_pass)

code, data = imap.list()
my_list = []
if code == "OK":
    for i in data:
        folder = i.decode('utf-8')
        first_ins = folder.find("\"/\"")
        nest_str = folder[first_ins:]
        second_ins = nest_str.find("\" \"")
        formatted_str = nest_str[second_ins:]
        mail_box = formatted_str[2:]
        MAILBOX = mail_box
        print(MAILBOX)
        my_list.append(MAILBOX)
        imap.select(MAILBOX)
        typ, data = imap.search(None, 'ALL', search_args)
        for num in data[0].split():
            print(num)
            imap.store(num, '+FLAGS', '\\Deleted')
            
    
    
imap.expunge()


imap.close()    
imap.logout()

