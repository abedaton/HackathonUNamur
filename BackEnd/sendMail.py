import smtplib
import email
from base64 import b64decode as bdc

#OurEmail = "hackathonunamur@gmail.com"

def dce(d):
    h=hex(d)[2:]
    b=bytes("".join([chr(int(h[i*2:i*2+2],16)) for i in range(len(h)//2)]),"utf-8")
    b=bdc(b)
    return b

def sendMail(data):
	msg = email.message_from_string(str(data))
	msg["From"] = OurEmail
	msg["To"] = OurEmail
	msg["Subject"] = "Message from a fan :D"
	sv = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	sv.ehlo()
	sv.starttls()
	sv.ehlo()
	sv.login(OurEmail, str(bdc(b"aGFja2F0aG9udW5hbXVyQGdtYWlsLmNvbQo="), "utf-8"))
	sv.sendmail(OurEmail, OurEmail, msg.as_string())

OurEmail  = "hackathonunamur@gmail.com"
password    = str(bdc(b"aGFja2F0aG9udW5hbXVyQGdtYWlsLmNvbQo="), "utf-8")
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
sendMail("Hello test")