# Clean Junk Email

Keeping your email's junk folder clean so you can find messages incorrectly identified as junk can be a challenge. This code searches through messages
in your junk folder and deletes messages where the sender or subject contain a string you specify. For example, you can delete all messages where 'viagra'
is in the subject or sender. 

## Prerequisites
1. You may need to enable IMAP access in your email settings.

2. If you have multi-factor authentication enabled on your account (which you should), you will need to set up a non-multifactor app password. Instructions for how to do this vary by provider. 

3. You will need to know the IMAP server for your email provider. For example, for Gmail, it is `imap.gmail.com`.

## Local Setup
1. Update the environment variables listed in `cleanjunk.py` by either adding them to your environment, or when running locally, creating a `.env` file based off `.env.sample` and setting them there.

    These variables are required:
    - `EMAIL_USERNAME`
    - `EMAIL_PASSWORD`
    - `EMAIL_IMAP_SERVER`

1. Put the list of phrases to look for in the email subject and sender, one per line, in the `junk_subjects.txt` and `junk_senders.txt` files, respectively.

1. Any email that does not have any addresses in the "to" field will be deleted. 

1. To install the dependencies, run `pip install -r requirements.txt`.

1. Run `python cleanjunk.py` to clean your junk folder. You will see an output showing the messages that were deleted, and which rule triggered them

## Sample Output
```
Junk emails: 40
('myemail.gmail.com',) formenonly<crew@formenonly.info> Get your viagra here!
IS JUNK: viagra
IS JUNK
==========
('myemail.gmail.com',) netflix, enjoy a year of netflix on us
IS JUNK: empty email
IS JUNK
==========
etc...
```