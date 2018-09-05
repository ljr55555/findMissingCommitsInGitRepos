################################################################################
##	This program searches a directory tree for git repositories and
## uses git diff-files to identify any local changes that have not been
## committed. 
##
## Author:	Lisa Rushworth
## Version:	1.0
## Date:	2018-09-04
## Revisions:	n/a
################################################################################
##      Editable variables
################################################################################
# String used when repo does not appear to be valid
strRepoError = "Invalid GIT repository"
strSenderAddress = "devnull@windstream.com"
#strRecipientAddresses = "lisa.rushworth@windstream.com"
#strMailRelay = "mail.windstream.com"
strRecipientAddresses = "lisa@rushworth.us"
strMailRelay = "fedora02.rushworth.us"	
iMailRelayPort = 25

# Import everything we need
import sys
import getopt

import os
from subprocess import check_output

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

def main(argv):

	strSearchRoot = ''

	try:
		opts, args = getopt.getopt(argv,"hd:",["dirname="])
	except getopt.GetoptError:
		print('Usage:\n\t_findMissingGitCommits.py -d <rootDirectoryToSearch>')
		sys.exit(2)

	if len(sys.argv) == 1:
		print('Usage:\n\t_findMissingGitCommits.py -d <rootDirectoryToSearch>')
		sys.exit(0)

	for opt, arg in opts:
		if opt == '-h':
			print('Usage:\n\t_findMissingGitCommits.py -d <rootDirectoryToSearch>')
			sys.exit()
		elif opt in ("-d", "--dirname"):
			strSearchRoot = arg

	strReposWithMissingCommits = [];

	for dirName, subdirList, fileList in os.walk(strSearchRoot):		
		if dirName.endswith("/.git"):											# Linux
			# strip .git and use that folder
			dirToProcess = dirName[:-4]
			print('Will diff directory %s' % dirToProcess)
			try:
				strResults = check_output(["bash", "-c" , 'cd %s;git diff-files' %dirToProcess])
			except:
				strResults = strRepoError

			if not strResults:
				pass
			elif strResults == strRepoError:
				print('Invalid git repository at %s' % dirToProcess)
			elif len(strResults) >= 1:
				strReposWithMissingCommits.append(dirToProcess)

		elif dirName.endswith("\\.git"):										# Windows
			# strip .git and use that folder
			dirToProcess = dirName[:-4]
			strCommand = "cd " + dirToProcess + "&git diff-files"

			try:
				strResults = check_output(strCommand, shell=True)
			except:
				strResults = strRepoError

			if not strResults:
				pass
			elif strResults == strRepoError:
				print('Invalid git repository at %s' % dirToProcess)
			elif len(strResults) >= 1:
				strReposWithMissingCommits.append(dirToProcess)


	if len(strReposWithMissingCommits) > 0:
		strMessageContent = "<table>"
		for strRepo in strReposWithMissingCommits:
			strMessageContent = strMessageContent + "<tr><td>" + strRepo + "</td></tr>"
			print('%s has uncommited changes' % strRepo)

		strMessageContent = strMessageContent + "</table>"
		
		mimeMsg = MIMEMultipart()
		mimeMsg['From'] = strSenderAddress
		mimeMsg['To'] = strRecipientAddresses
		mimeMsg['Subject'] = "GIT Repos With Outstanding Commits"
		mimeMsg.attach(MIMEText(strMessageContent,'html'))

		smtpServer = smtplib.SMTP(strMailRelay, iMailRelayPort)
		#smtpServer.set_debuglevel(True)
		smtpServer.ehlo()
		smtpServer.starttls()
		smtpServer.ehlo()
		strMessageText = mimeMsg.as_string()
		smtpServer.sendmail(strSenderAddress, strRecipientAddresses, strMessageText)

if __name__ == "__main__":
   main(sys.argv[1:])