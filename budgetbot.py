from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from bs4 import BeautifulSoup as bs4
from pyparsing import htmlComment


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
        messages = results.get('messages', []) #max length 100

        found = 0
        total = 0   
        for i in range(100):
            msg = service.users().messages().get(userId='me', id=messages[i]['id']).execute()
            From, Subject, Date = getFromSubjectDate(msg)
            if From == 'transaccionesbg@bgeneral.com':
                html = getEmailHtml(msg)
                text = getHTMLText(html)
                money = float(getMoney(text))
                total += money
                found += 1
                print("From: ", From)
                print("SUBJECT: ", Subject)
                print("DATE: ", Date)
                print("MONEY: ", money)
                print("------")

        # print("Found: ", found)
        # print("Total: ", total)

    except:
        pass    

    #from index = 13
    #subject index = 15
    #date index = 16

def getMoney(text):
    for i in text:
        if i[0] == '$':
            return i[1:]


def getHTMLText(html):
    soup = bs4(html, 'html.parser')
    #find the money amount
    text = soup.get_text()
    text = text.replace('\\r', '').replace('\\n', '').replace('\\t', '').replace(' ', ',')
    text = text.split(',')
    text = [x for x in text if x != '']
    return text


def getEmailHtml(msg):
    return base64.urlsafe_b64decode(msg['payload']['body']['data'])


def getFromSubjectDate(msg):
    From = ''
    Subject = ''
    Date = ''
    for index, item in enumerate(msg['payload']['headers']):
        if item['name'] == 'Subject':
            Subject = item['value']
        elif item['name'] == 'From':
            From = item['value']
        elif item['name'] == 'Date':
            Date = item['value']
    return From, Subject, Date


if __name__ == '__main__':
    main()
