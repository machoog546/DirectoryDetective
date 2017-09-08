#Directory Detective

Directory watcher that keeps an eye on network folders in it's parent direcotry. Checks again after 15 min, and if a folder is missing it send an email to someone through MS Outlook.

#Getting Started

Used modules are as followed:
-os
-datetime
-win32com.client
-time

#Prerequisites

Install win32com from 'https://pypi.python.org/pypi/pywin32' by downloading and instaling from the exe (or whatever package is needed for Linux/OSX).

#Installing

Install win32com, and open the script in a text editor and update the "directoryToWatch" to what parent folder you want to keep an eye on, and the "mail.To" field. Seperate emails with a ";" between addresses on the same line.

After doing these changes run the code and it will scan the folder for its "baseline" after 15 min you will see it do the compare. If something is wrong an email will be sent to the addresses in the "mail.to" variable.

#Built With

Used code/examples from the following sources:
-https://stackoverflow.com/questions/8440446/sending-email-with-python-smtplib-not-working-confused-about-the-from-field
-https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
-https://github.com/dbader/schedule/blob/master/schedule/__init__.py
-https://stackoverflow.com/questions/38825824/checking-time-for-executing-if-statement

#Authors

Sam Machuga - Initial work - Machoog546
Eric Nuno - Peer review

#Acknowledgments

Hat tip to anyone who's code was used
Inspiration/suggestion for me to use this as practice - Eric Nuno
