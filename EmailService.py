# provide email related functionality.

# user send email, whose subject should be: "request", body include:
# "yourskypename".

import time
import email, imaplib, os, random
import smtplib
import subprocess



from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders




global Eaddr,passwd
Eaddr = "magiclamp1000@gmail.com"
passwd = "202154215471"

def Branch(mail):
    if mail["Subject"] == "search":
        VideoSearch(mail)
        return 1
    if mail["Subject"] == "url":
        UrlHandle(mail)
        return 1
    elif mail["Subject"] == "myemail":
        MyemailHandle(mail)
    elif mail["Subject"] == "add":
        AddHandle(mail)
        return 0

def VideoSearch(mail):
    query = BodyOneLine(mail)
    Url = "https://www.google.com/search?tbm=vid&q="
    for each_term in query.split(" "):
        Url = Url + "+" + each_term
    print Url
    proc = subprocess.Popen(["phantomjs", "rasterize.js", Url, "temp.pdf"])
    proc.wait()
    print "search finished"
    MailAttach(mail["From"], "Search Result", "temp.pdf")
    print "PDF file has been sent!"

def AddHandle(mail):
    f = open("AddFriend", "r+")
    old = f.read()
    f.seek(0)
    left = mail["From"].index("<")+1
    right = mail["From"].index(">")
    package = mail["From"][left:right] + " " + BodyOneLine(mail) + "\n"
    f.write(package + old)
    f.truncate()
    f.close()
    MailBack(mail["From"][left:right], BodyOneLine(mail) + "has been allowed to join the service! Please let him add server into his contact list!", "Adding friend succeeds!")

def MyemailHandle(mail):
    f = open("Pending","r+")
    old = f.read()
    f.seek(0)
    left = mail["From"].index("<") + 1
    right = mail["From"].index(">")
    source = mail["From"][left:right]
    Skyname = BodyOneLine(mail).split()[0]
    Passcode = BodyOneLine(mail).split(" ", 1)[1]
    f.write(Skyname + " " + source + " " + Passcode + "\n" + old)
    f.close
    MailBack(mail["From"], "Success!", "Pending!")



def EmailCheck(mail):
    left = mail["From"].index("<")
    right = mail["From"].index(">")
    source = mail["From"][left + 1:right]

    f= open("EmailCheck","r")
    lines = f.readlines()
    for line in lines:
        if source in line:
            return line.split(" ")[0]
    return 0


def UrlHandle(mail):
    name = EmailCheck(mail)
    if name != 0:
        f= open("JobList", "wa")
        print BodyOneLine(mail)
        f.write(name + " " + BodyOneLine(mail) + "\n")
        f.close
        MailBack(mail["From"], "Success!","On Queue!")
    else:
        MailBack(mail["From"], "Wrong!", "Please Register!")

def BodyOneLine (msg):
    maintype = msg.get_content_maintype()
    if maintype == 'multipart':
        for index, part in enumerate(msg.walk()):
          if index == 1:
            return part.get_payload().split("\n")[0]

    elif maintype == 'text':
        return msg.get_payload().split("\n",1)[0]



def MailAttach(Who, Subject, Atpath):

    global Eaddr, passwd
    fromaddr = Eaddr
    toaddrs = Who
    username = Eaddr.split("@")[0]
    password = passwd

    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = fromaddr
#    msg['To'] = ', '.join(toaddrs)
    msg['To'] = toaddrs

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(Atpath, "rb").read())
    Encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename=' + Atpath)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()



def MailBack(Who, Msg, Subject):
    global Eaddr, passwd
    fromaddr = Eaddr
    toaddrs  = Who
    username = Eaddr.split("@")[0]
    password = passwd

    headers = ["from: "+ fromaddr, "subject: "+ Subject]
    headers = "\r\n".join(headers)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, headers + "\r\n\r\n" + Msg)
    server.quit()



def init():
    if not os.path.exists("Pending"):
        f = open("Pending", "w")
        f.write("\n")
        f.close
    if not os.path.exists("EmailCheck"):
        f= open("EmailCheck", "w")
        f.write("\n")
        f.close
    if not os.path.exists("JobList"):
        f = open("JobList", "w")
        f.write("\n")
        f.close
    if not os.path.exists("AddFriend"):
        f = open("AddFriend", "w")
        f.write("\n")
        f.close
    return 1

init()
while 1:
    time.sleep(2)
    detach_dir = '.' # directory where to save attachments (default: current)
    user = Eaddr.split("@")[0]
    pwd = passwd

# connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes


    resp, items = m.search(None, "UNSEEN") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)

    items = items[0].split() # getting the mails id

    for emailid in items:
        resp, data = m.fetch(emailid, "RFC822") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

        print mail["Subject"]


        Branch(mail)

#    print showme(mail)
