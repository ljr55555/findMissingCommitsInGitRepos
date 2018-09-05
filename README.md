# Find uncommited changes in local git repos under a subtree
As our group adopts a software development methodology, I have encountered a *LOT* of instances where someone "forgets" to go through the extra steps of ensuring the Git repository is up to date.

Searches have yielded many scripts that parse "git status" output to identify where a local repo is not in sync with the server repo. These, unfortunately, seem to break as the git status output format changes. And they are overkill for *my* problem -- files are changed on disk but not added, committed, *or* pushed upstream.

This script uses "git diff-files" to verify that files on disk (in the local repo) match up with the index (in the local repo) and sends an e-mail alert when uncommitted changes are identified. 

# Usage
To simplify usage across multiple servers, parameters define the root directory, mail relay, notification sender, and notification recipient(s) addresses. 
* *pythonBinary* _findMissingGitCommits.py -d \<rootDirectoryToSearch\> -m \<smtpRelay\> -p \<smtpPort\> -s \<senderAddress\> -r \<recipientAddresses\>
     
E.G.
* python3.6 _findMissingGitCommits.py -d /Scripts -m mail.domain.ccTLD -p 587 -s "lisa@domain.ccTLD" -r "someone@domain.ccTLD"
     

