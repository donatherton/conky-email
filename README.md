# conky-email
Polls an imap server for unread emails and displays in Conky

Queries server and gets unread email from and subject fields and displays in Conky.
Usage: set Conky to update every whatever minutes. Not every second!!
username and imap server fields mandatory, the rest optional, as long as password is in keyring

${execp ~/path/to/conky/donmail.py --username=you@example.com --password=your-password --imap_host=imap.example.com --port=xxxx --limit=integer number of emails to show}
