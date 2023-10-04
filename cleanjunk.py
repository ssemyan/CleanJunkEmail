import os
from imap_tools import MailBox
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# account credentials
EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_IMAP_SERVER = os.environ.get("EMAIL_IMAP_SERVER")

# need to set env variables
if not EMAIL_USERNAME or not EMAIL_PASSWORD or not EMAIL_IMAP_SERVER:
    raise Exception("Need to set EMAIL_USERNAME, EMAIL_PASSWORD and EMAIL_IMAP_SERVER environment variables")

# load file into array of values
with open('junk_senders.txt', 'r') as file:
    junk_senders = [line.strip() for line in file if not line.startswith('#')]

with open('junk_subjects.txt', 'r') as file:
    junk_subjects = [line.strip() for line in file if not line.startswith('#')]

# Get date, subject and body len of all emails from INBOX folder
with MailBox(EMAIL_IMAP_SERVER).login(EMAIL_USERNAME, EMAIL_PASSWORD) as mailbox:
    
    # show all folder names
    # for f in mailbox.folder.list():
    #    print(f)
    
    # show number of junk mails
    stats = mailbox.folder.status('Junk')
    print(f"Junk emails: {stats['MESSAGES']}")  # {'MESSAGES': 41, 'RECENT': 0, 'UIDNEXT': 11996, 'UIDVALIDITY': 1, 'UNSEEN': 5}

    mailbox.folder.set('Junk')
    for msg in mailbox.fetch():
        from_value = msg.from_values.full.lower().replace(' ', '')
        # remove any unicode characters
        from_value = from_value.encode('ascii', 'ignore').decode('ascii')
        print(msg.to, from_value, msg.subject)
        is_junk = False

        # senders with empty email addresses are junk (can optionally check if email is sent to me)
        if msg.from_values.email == '': # or str(msg.to).lower().find(EMAIL_USERNAME) == -1:
            print(f'IS JUNK: empty email')
            is_junk = True

        if not is_junk:
            for sender in junk_senders:
                if from_value.find(sender.replace(' ', '').lower()) != -1:
                    print(f'IS JUNK: {sender}')
                    is_junk = True
                    break

        if not is_junk:
            subject = msg.subject.lower().replace(' ', '')
            for subj in junk_subjects:
                if subject.find(subj.replace(' ', '').lower()) != -1:
                    print(f'IS JUNK: {subj}')
                    is_junk = True
                    break

        if is_junk:
            print('IS JUNK')
            mailbox.move(msg.uid, "Deleted")
        
        print("="*10)
