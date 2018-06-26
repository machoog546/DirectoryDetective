"""
Who: Any user that has read access to a folder/network drive.
What: This script is used to keep an eye on folders in a network share by scanning the folder and getting a baseline of what folders were there. After some time it would check again and compaire to first list.
Where: Can be ran on local machine, or part of bigger script if wanted.
When: Default check time is every 5 min.
Why: A folder share for our IT department would randomly be missing folder. Users would accidently move folders into other folders. This would send an alert saying the folder was "mising."
    We talked about making it search for the folder's "new" location after one went missing, but we never implimented it and just did a search in Windows/Linux as needed.
"""

import os #needed for os.walk
import datetime #weekday setup
import smtplib #needed for smtp email send
from time import sleep  #needed for the 300-ish second sleep


directoryToWatch = "//fileshare.company.com/folder/Network_repository" #
departmentFolder = "//prd1nas.company.com/departmentFolder"
#currentLocation = os.getcwd() #TESTING ONLY#-change if script is running somewhere else you dont want to save a file to

"""
This script would watch two folders at one time:
    -The departmentFolder folder was a parent direcotry that had several department's folder residing there.
    -directoryToWatch was a specific departments folder where thre were several accidental folder moves a week
"""

def issue_message(theMissing, theLeftovers, other):

    print("Sending email. Root QA drive has issues.\n")

    to = ["user1@company.com", "user2@company.com"]
	from_field = "Directory.Detective@company.com" #this can be a dummy email if needed. Tested with MS Outlook server
    message = """From: Directory Detective <Directory.Detective@company.com>
    To: First Last user1@company.com>
    Subject: QA folder alert.
Network QA root folder experencing issues: \n"""

    if len(other) > 0: #the string of other, when assigned, will always be greater than 0.
        if len(other) == 1 and  "not be reachable" in other[0]:
            message += str(other)
        else:
            message += str(other)

    if len(theMissing) > 0:
        message += "The following are missing folders in the root drive: \n" + str(theMissing) + "\n"

    if len(theLeftovers) > 0:
        message = message[:-44]
        message += "The following folders are 'new': \n\t" + str(theLeftovers)


    server = smtplib.SMTP("x.x.x.x", "xxxx") #Ip address/hostname of mail server, port number
    server.sendmail(from_field, to, message)
    server.quit()


    return

def QA_folder_reachable(dirList):

    other = []
    if os.path.isdir(departmentFolder) == True: #checks if m drive is reachable at full folder path
        theMissing = [] #list of missing files in root QA folder
        theLeftovers = [] #list of "extra" or new folders in root QA folder
        mDriveFolders = next(os.walk(departmentFolder))[1] #gets a list of current folders in root QA
        neededFolders = ['Network_repository', 'Hardware_repository', 'Automation_Services', '~snapshot'] #this is a list of folders that need to be in the departmentFolder. If any of these are missing there would be seperate alert.

        if len(mDriveFolders) == 0:
            print("QA path might not be readable. Check connectivity.")


        if len(mDriveFolders) != 4: #change if folder added or removed perminantly
            for item in neededFolders:
                try: #try to remove item from needed folders list.
                    mDriveFolders.remove(item)
                except: #if folder not there, append to dirList
                    theMissing.append(item)

            if len(mDriveFolders) > 0:
                for item in mDriveFolders:
                    theLeftovers.append(item)

        if len(theMissing) > 0 or len(theLeftovers) > 0:
            issue_message(theMissing, theLeftovers, other)

    else:
        other = ["Root QA drive might not be reachable."]
        theMissing = []
        theLeftovers = []
        issue_message(theMissing, theLeftovers, other)


def runEvery5():

    missingFileMaybe = []
    dirList = []
    theMissing = []
    theLeftovers = []
    other = []
    try:
        dirList = os.listdir(directoryToWatch) #this will "walk" down the direcotry and get a list of folders
        print("\nCurrent list of files:\n" + str(dirList))
        print("\nTime of check " + str(datetime.datetime.now()))

    except:
        if len(dirList) == 0:
            QA_folder_reachable(dirList)
            sleep(293) #leave this, or a loop of bad things...many emails
            return

    if "New folder" in dirList: #if New folder in list, kick out email
        other = ["New folders found in QA drive. Please Verify"]
        print("New Folder found. Sending alert\n")
        issue_message(theMissing, theLeftovers, other)
        other = []

    sleep(293) #300sec = 5min - 5s for wait - 2s for script delta (rough guess)

    try:
        after5List  = os.listdir(directoryToWatch)
    except:
        print("Cannot read QA after 5 min")
        other = ["Root QA drive might not be reachable."]
        theMissing = []
        theLeftovers = []
        issue_message(theMissing, theLeftovers, other)
        sleep(293)
        return

    print("\nChecking aginst:\n" + str(after5List))
    for d in dirList:
        try:
            after5List.remove(d)
        except:
            missingFileMaybe.append(d)

    if len(missingFileMaybe) > 0:
        sendEmail(missingFileMaybe)
        print("\n----\nFolder(s) moved:\n"+ str(missingFileMaybe) +  "\n----\n")
    else:
        print("Directory Detective has found no issues.")
    print("\nTime of check " + str(datetime.datetime.now()))

    if len(after5List) > 0: #alert saying new folder
        for folder in after5List:
            theLeftovers.append(folder)

        issue_message(theMissing, theLeftovers, other)
        theLeftovers = []


        print("New folder(s) found: \n")
        for folders in after5List:
            print("\t"+folder)


    sleep(5)

def sendEmail(missingFileMaybe):

	to = ["User1@company.com", "user2@company.com"]
	from_field = "Directory.Detective@company.com" #this can be a dummy email if needed. Tested with MS Outlook server

	TheBody = "The following folder(s) appear to be missing: \n" + str(missingFileMaybe)

	Subject = "Folders have moved.\r\n"
	message = 'Subject: {}\n\n{}'.format(Subject, TheBody)
	msg = ("From: %s\r\nTo: %s\r\n"
	% (from_field, ", ".join(to)))
	msg = msg + message


	server = smtplib.SMTP("x.x.x.x", "xxxx") #Ip address/hostname of mail server, port number
	server.sendmail(from_field, to, msg)
	server.quit()

while True:

    now = datetime.datetime.now()
    if datetime.datetime.today().weekday() != 5 and datetime.datetime.today().weekday()!= 6:
        if now.hour > 7 and now.hour < 18:
            runEvery5()
            #input("enter") #debug only -- Remove when going into prod.





"""
Changes needed before being put into prod
-change emails back to eric, or to the PE distros
"""
"""
https://stackoverflow.com/questions/8440446/sending-email-with-python-smtplib-not-working-confused-about-the-from-field
https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
https://github.com/dbader/schedule/blob/master/schedule/__init__.py
https://stackoverflow.com/questions/38825824/checking-time-for-executing-if-statement
"""
