################################################################################
##      Editable variables
################################################################################
# Root from which to search for git repos
strSearchRoot = '/bhs00p10/Scripts'
# String used when repo does not appear to be valid
strRepoError = "Invalid GIT repository"
strSenderAddress = "devnull@windstream.com"
strRecipientAddresses = "lisa.rushworth@windstream.com"
strMailRelay = "mail.windstream.com"
iMailRelayPort = 25

# Import everything we need
import os
from subprocess import check_output
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 


strReposWithMissingCommits = [];

for dirName, subdirList, fileList in os.walk(strSearchRoot):
	if dirName.endswith("/.git"):
#		print('Found git directory %s' % dirName)
		# strip .git and use that folder
		dirToProcess = dirName[:-4]
#		print('Will diff directory %s' % dirToProcess)
		try:
			strResults = check_output(["bash", "-c" , 'cd %s;git diff-files' %dirToProcess])
		except:
			strResults = strRepoError
	
		if not strResults:
			pass
#			print('%s has no uncommitted changes' % dirToProcess)
		elif strResults == strRepoError:
			print('Invalid git repository at %s' % dirToProcess)
		elif len(strResults) >= 1:
#			print('%s has uncommitted changes' % dirToProcess)
			strReposWithMissingCommits.append(dirToProcess)

if len(strReposWithMissingCommits) > 1:
	strMessageContent = ""
	for strRepo in strReposWithMissingCommits:
		strMessageContent = strMessageContent + "<tr><td>" + strRepo + "</td></tr>"
		print('%s has uncommited changes' % strRepo)
	
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

