#!/usr/bin/python

import os
import sys
import smtplib
import mimetypes
from email.Encoders import encode_base64
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# =====================================
# CONFIG

DEBUG = False
# DEBUG = True

MAIL_FROM = 'zfsmon@localhost'
MAIL_TO = 'test@localhost'
MAIL_HOST = 'localhost'
MAIL_PORT = 1025 # 465 SSL/TLS
MAIL_USER = 'zfsmon'
MAIL_PASS = 'password'

MAIL_ALL_OK = True # Even send an EMail if everything is OK
# MAIL_ALL_OK = True # Even send an EMail if everything is OK

CMD_ZPOOL = 'sudo /sbin/zpool'

# =====================================
# LIB

# open a connection to the SMTP-Server
def initSMTP():
  try:
    # USE SSL/TLS INSTEAD
    # s = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
    s = smtplib.SMTP(MAIL_HOST, MAIL_PORT)

    # DETAILED TRACE
    #s.set_debuglevel(1)
    s.ehlo()    
    s.login(MAIL_USER, MAIL_PASS)
    return s
  except Exception, e:
    print e
    sys.exit(1)

# close the SMTP-connection
def closeSMTP(s):
  s.quit()
  s.close()

# send an E-Mail using specified SMTP-Connection
def sendMail(subj, body):
  try:
    # connect to SMTP
    s = initSMTP()

    msg = MIMEMultipart()
    msg['From']    = MAIL_FROM
    msg['To']      = MAIL_TO
    msg['Subject'] = subj
    msg.attach(MIMEText(body))
	
    s.sendmail(MAIL_FROM, MAIL_TO.split(";"), msg.as_string())
    closeSMTP(s)
  except Exception, e:
    print e
    sys.exit(1)

# execute a command and return its output
def cmd(c):
  try:
    proc = os.popen(c)
    out  = proc.read().strip()
    return out
  except Exception, e:
    print e
    sys.exit(1)

# create a summary-text of failed-command's output and additional details
def summary(failed, details):
  s  = failed
  s += "\n----------\n\n"
  s += details
  return s


# =====================================
# MAIN()
alert = False

# ZFS Pool checking
zpoolStatusX = cmd(CMD_ZPOOL + ' status -x')
# IF pools are not healthy or debug TEST flag is set, send out email alert
if DEBUG or zpoolStatusX.find("all pools are healthy") == -1:
  alert = True
  zpoolStatus = cmd(CMD_ZPOOL + ' status')
  txt = summary(zpoolStatusX, zpoolStatus)
  sendMail("[NAS] ZFS Pool Status", txt)

# IF pools are healthy and mail flag is set send out email
if alert == False and MAIL_ALL_OK == True:
  sendMail("[NAS] O.K.", "Everything is fine")

sys.exit(0)
