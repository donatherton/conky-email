#!/usr/bin/env python3
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: Don Atherton
# Web: https://donatherton.co.uk
# WeatherWidget (c) Don Atherton don@donatherton.co.uk
"""
Queries server and gets unread email from and subject fields and displays in Conky.
Usage: set Conky to update every whatever minutes. Not every second!!
username and imap server fields mandatory, the rest optional, as long as password is in keyring

${execp ~/path/to/conky/donmail.py --username=you@example.com --password=your-password --imap_host=imap.example.com --port=xxxx --limit=integer number of emails to show}
"""
import imaplib
import re
from email.header import decode_header
import keyring
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--username',nargs=1,required=True)
parser.add_argument('--imap_host',nargs=1,required=True)
parser.add_argument('--password',nargs=1,required=False)
parser.add_argument('--port',nargs=1,required=False)
parser.add_argument('--limit',nargs=1,required=False)

try:
	args = parser.parse_args()
except:
	print('Need a username and/or imap server')

username = args.username[0]
imap_host = args.imap_host[0]
try:
	port = args.port[0]
except:
	port = 993

if args.password:
	password = args.password[0]
else:
	try:
		password = keyring.get_password("conky", username)
	except:
		print("Can't retrieve password from keyring")

try:
	limit = args.limit[0]
except:
	limit = 5

def decodeHeader(header_text):
        text,encoding = decode_header(header_text)[0]
        if encoding:
            try:
                return text.decode(encoding)
            except: # fallback on decode error to windows encoding as this may be introduced by sloppy mail clients
                return text.decode('cp1252')
        else:
            return text
# connect
try:
	imap = imaplib.IMAP4_SSL(imap_host)
	imap.login(username, password)
except:
	try:
		imap = imaplib.IMAP4(host=imap_host, port=port)
		imap.login(username, password)
	except:
		print("Can't get through :(")
		exit(1)
try:
	imap.select("INBOX")
	messages = imap.search(None,'UNSEEN')
	for message in messages:
		        if messages != None and len(messages) > 0:
		            nums = messages[1][0].split()
		            count = (len(nums))
		        else:
		            count = 0
	print(username + ": " + str(count) + "${alignr}" + datetime.now().strftime('%H:%M'))
	if count > 0:
		i = 1
		for num in reversed(nums):
					status, message_info = imap.fetch(num, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])')
					message_info = message_info[0][1].decode('utf-8')
					sender = re.search('From:.*\n',message_info)
					sender =  decodeHeader(sender[0][6:].strip())
					subject = re.sub('From:.*\n','',message_info) # remove sender line, leaving subject
					if subject != None:
						subject = str(decodeHeader(subject[9:].strip()))
					else:
						subject = 'No subject'
					output = sender + " -- " + subject
					print("${voffset 6}" + output)
					i = i+1
					if i > int(limit): #Stop at limit. That'll do.
						break
except Exception as e:
	print("Can't retrieve messages :(", e)
imap.close()
imap.logout()
