import os #needed for os.walk
import datetime #weekday setup
import smtplib #needed for smtp email send
from time import sleep  #needed for the 900-ish second sleep


directoryToWatch = "C:/path/to/parent/folder" #
#

def runEvery15():
    missingFileMaybe = []
    dirList = next(os.walk(directoryToWatch))[1] #this will "walk" down the direcotry and get a list of folders
    print("\nCurrent list of files:\n" + str(dirList))

    sleep(893) #900sec = 15min - 5s for wait - 2s for script delta (rough guess)

    after15List  = next(os.walk(directoryToWatch))[1]
    print("\nChecking aginst:\n" + str(after15List))

    for d in dirList:
        try:
            after15List.remove(d)
        except:
            missingFileMaybe.append(d)
    if len(missingFileMaybe) > 0:
        sendEmail(missingFileMaybe)
        print("\n----\nFolder(s) moved:\n"+ str(missingFileMaybe) +  "\n----\n")
    else:
        print("Directory Detective has found no issues.")
    sleep(5)


def sendEmail(missingFileMaybe):

    #subject = "Test Email"
    to = "username@email.com"
    from_field = "username@email.com"
    body = "The following folder(s) appear to be missing:\n" + str(missingFileMaybe)
    server = smtplib.SMTP("x.x.x.x", "port#X")
    server.sendmail(from_field, to, body)
    server.quit()


while True:
    now = datetime.datetime.now()
    if datetime.datetime.today().weekday() != 5 and datetime.datetime.today().weekday()!= 6:
        if now.hour > 7 and now.hour < 18:
            runEvery15()
            #input("enter") #debug only -- Remove when going into prod.



"""
https://stackoverflow.com/questions/8440446/sending-email-with-python-smtplib-not-working-confused-about-the-from-field
https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
https://github.com/dbader/schedule/blob/master/schedule/__init__.py
https://stackoverflow.com/questions/38825824/checking-time-for-executing-if-statement
"""
