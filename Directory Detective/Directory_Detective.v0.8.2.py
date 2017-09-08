import os #needed for os.walk
import datetime #weekday setup
import win32com.client as win32 #needed for outlook email
from time import sleep  #needed for the 900-ish second sleep


directoryToWatch = "C:/Path/To/Folder" #
#
missingFileMaybe = []
def runEvery15():

    dirList = next(os.walk(directoryToWatch))[1] #this will "walk" down the direcotry and get a list of folders
    print("Current list of files:\n" + str(dirList))

    sleep(893) #900sec = 15 - 5 for wait - 2 for script delta (rough guess)

    after15List  = next(os.walk(directoryToWatch))[1]
    if len(missingFileMaybe) < 1:
        print("Checking aginst:\n" + str(after15List))

    for d in dirList:
        try:
            after15List.remove(d)
        except:
            missingFileMaybe.append(d)
    if len(missingFileMaybe) > 0:
        sendEmail()
        print("These gone:\n"+ str(missingFileMaybe))
    else:
        print("Everything is good. Move along.")
    sleep(5)


def sendEmail():

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'email@example.com'
    #mail.CC = 'emal@example.com'
    mail.Subject = 'Holy missing directory, Batman!'

    TheBody = "The following folders appear to be missing:\n" + str(missingFileMaybe)
    mail.body = TheBody
    mail.send


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
