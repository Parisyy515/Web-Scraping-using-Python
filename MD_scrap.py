Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@Parisyy515 
Parisyy515
/
FilesExchange
Private
1
00
Code
Issues
Pull requests
Actions
Projects
1
Security
Insights
Settings
FilesExchange/immunetScraper.py /
@Parisyy515
Parisyy515 Add files via upload
Latest commit ebb4554 12 minutes ago
 History
 1 contributor
438 lines (333 sloc)  14.6 KB
  
#Filename: immunetScraper.py
#Author: Kelly Dolan
#Purpose: Grabbing immunization records from Maryland immunnet website.
#
#Class List: -Person (firstName, lastName, dateOfBirth, gender, memberId)
#               -Constructor (initializer)
#				-Getters:
#                  - getMeasYr, getMemberIdSkey, getMemberId,getFirstName,
#					 getLastName, getDateOfBirth, getGender
#
#Global functions:
#			 -findHidden (request)
#				-Returns dictionary of all hidden form fields
#
#			 -getString (recordFound)
#				-Returns a concatenated string to write to spreadsheet
#
#			 -stripSuffix (lname)
#               -Strips away name suffixes like Jr., II., etc.
#                 -These suffixes aren't used in the registry, so not removing them would result in
#                  not getting a hit on a record.  
#               -This reads in a file that contains a list of common name suffixes.
#                 -The file name is read as Suffixes.xlsx
#
#            -printStats()
#                -Runs at end of program to display run time and # of people found
#
#User Input:
#	         -First input: CSV file name that contains the following information in this order:
#		        -measYr, memberId, memberIdSkey, firstName, lastName, suffix, dob,   gender, stateRes, (Meas)
#               -col A,  col B,    col C,        col D,     col E,    col F,  col G, col H,  col I,    (col J)
#            -Second input: Line to start reading from (To start at beginning input 0)
#                -(This was added as a precaution if the program or website times out halfway)
#            -Third input: Username for immunnet
#            -Fourth input: Password for immunnet
##############################################################################

#Imports
import requests
import lxml.html
import csv
import bs4
import getpass
import datetime
import sys
import time

##############################################################################

#Classes
class Person(object):
    def __init__(self, measYr, memberId, memberIdSkey, fname, lname, lnameSuffix, dob, gender, stateRes, meas):
		self.measYr = measYr
		self.memberId = memberId
		self.memberIdSkey = memberIdSkey
		self.fname = fname
		self.lname = lname
		self.lnameSuffix = lnameSuffix
		self.dob = dob
		self.gender = gender
		self.stateRes = stateRes
		self.meas = meas
		
    def getMeasYr(self):
		return self.measYr
		
    def getMemberIdSkey(self):
        return self.memberIdSkey	
		
    def getMemberId(self):
		return self.memberId
		
    def getFirstName(self):
        return self.fname
		
    def getLastName(self):
        return self.lname

    def getLastNameSuffix(self):
		return self.lnameSuffix
		
    def getDateOfBirth(self):
        return self.dob
	
    def getGender(self):
		return self.gender

    def getStateRes(self):
		return self.stateRes
	
    def getMeas(self):
		return self.meas
		
##############################################################################

#Functions
def findHidden (request):
	html = lxml.html.fromstring(request.text)
	#Using regEx to grab all hidden input forms
	hiddenInputs = html.xpath(r"//form//input[@type='hidden']")
	creds = {x.attrib["name"]: x.attrib["value"] for x in hiddenInputs}
	return creds

def getString(recordFound):
	lname = p.getLastName()
	if (len(p.getLastNameSuffix()) > 0):
		lname += ' ' + p.getLastNameSuffix()
		
	if (recordFound == 0):
		str = (p.getMeasYr() + ',' + p.getMemberIdSkey() + ',' + p.getMemberId() + ',' + 
		p.getFirstName() + ',' + lname + ',' + p.getDateOfBirth() + ',' + p.getGender() + 
		',' + p.getStateRes() + ',MD')

	else:
		str = (p.getMeasYr() + ',' + p.getMemberIdSkey() + ',' + p.getMemberId() + ',' + 
		p.getFirstName() + ',' + lname + ',' + p.getLastNameSuffix() + ',' + p.getDateOfBirth() + ',' + p.getGender() + 
		',' + p.getStateRes() + ',MD')
		
		print('Record not found.')
	
	return str
		
#Currently not being called - checks for suffixes are removed before input is fed into script
#Logic kept for possible future needs
def stripSuffix (lname):
	i = 0
	while i < longestSuffixLength:
		if lname[-i:].upper() in suffixArray:
			lname = lname[:-i]
		i += 1
	
	return lname
	
def printStats ():
	percentageOfMiss = float(notFound) / float(totalPeople) 
	percentageOfHits = float(totalHits) / float(totalPeople)
	missRounded = round(percentageOfMiss, 2)
	hitsRounded = round(percentageOfHits, 2)
	missStr = str(missRounded * 100) + '%'
	hitsStr = str(hitsRounded * 100) + '%'

	print('\n-------------------FINISHED-------------------\n')
	print('-----------------RECORD STATS-----------------')
	print('Number of lookups           : ' + str(totalPeople).rjust(15))
	print('Number of records found     : ' + str(totalHits).rjust(15))
	print('Number of records not found : ' + str(notFound).rjust(15))
	print('Percentage rate of hits     : ' + hitsStr.rjust(15))
	print('Percentage rate of misses   : ' + missStr.rjust(15))

	print('\n------------------TIME STATS------------------')
	duration = endTime - startTime
	print('Scraping began at: ' + str(startTime))
	print('Scraping ended at: ' + str(endTime))
	print('Total time taken : ' + str(duration).rjust(26))
	
##############################################################################
	
#Welcome message/how to use
print('\nThis is the web scraper for the MaryLand Immunization Record Website.')
print('You will be prompted to type in a file name and username/password.')
print('If you need to exit the script and stop its process press \'CTRL\' + \'Z\'.') 
	
#Grab search criteria from user input spreadsheet
fileName = raw_input("\nEnter file name: ")

#Adds extension if not present
if (fileName[-4:] != '.csv'):
	fileName += '.csv'

#If file doesn't exist, exit program
try:
	file = open(fileName, 'rb')
except:
	print('File Not Found\n')
	sys.exit()
	
#Which line to start on
indexNumber = raw_input("\nStart on line (include headers): ")

print('\nReading file, please wait.\n')

reader = csv.reader(file, delimiter=',')
#Skip headers
reader.next()

#Create array of People objects
peopleArray = []
memberIdArray = []

#Columns needed: MeasureYear: A(0), MemberID: B(1), MemberIDSkey: C(2), FirstName: D(3), LastName: E(4), LastNameSuffix: F(5), 
#                DateOfBirth: G(6), Gender: H(7), StateRes: I(8), Meas: J(9) 

for row in file:

	t = row.split(',')
	m = t[1]
	
	inputDate = str(t[6])
	
	#If date is null then assign an impossible date
	if not inputDate:
		inputDate='01/01/1900'
		
	if '-' in inputDate:
		correctDateFormat = datetime.datetime.strptime(inputDate, '%Y-%m-%d').strftime('%m/%d/%Y')
	else:
		correctDateFormat = datetime.datetime.strptime(str(t[6]), '%m/%d/%Y').strftime('%m/%d/%Y')
	
	p = Person (t[0], t[1], t[2], t[3], t[4], t[5], correctDateFormat, t[7], t[8], t[9])	

	if (m not in memberIdArray):
		peopleArray.append(p)
		
	memberIdArray.append(m)

file.close()

###################################################################################

#Create worksheet to write to

date = str(datetime.date.today())
fileOutputName = 'HEDIS_Immun_Records_' + date.replace('-', '_') + '.csv'
fileOutputNameNotFound = 'HEDIS_Immun_Records_Not_Found_' + date.replace('-', '_') + '.csv'

fileOutput = open(fileOutputName, 'w')
fileOutputNotFound = open(fileOutputNameNotFound, 'w')

#Creating column headers
fileOutput.write('MEAS_YR,MEMB_LIFE_ID_SKEY,MEMB_LIFE_ID,MEMB_FRST_NM,MEMB_LAST_NM,'+
'DOB,GNDR,RSDNC_STATE,IMUN_RGSTRY_STATE,VCCN_GRP,VCCN_ADMN_DT,DOSE_SERIES,'+
'BRND_NM,DOSE_SIZE,RCTN\n')

fileOutputNotFound.write('MEAS_YR,MEMB_LIFE_ID_SKEY,MEMB_LIFE_ID,MEMB_FRST_NM,MEMB_LAST_NM,MEMB_SUFFIX,'+
'DOB,GNDR,RSDNC_STATE,IMUN_RGSTRY_STATE,VCCN_GRP,VCCN_ADMN_DT,DOSE_SERIES,'+
'BRND_NM,DOSE_SIZE,RCTN\n')

###################################################################################

#FIRST PAGE: LOGIN SCREEN

#Create connection to Immunet
#Login process: Form Action, Username, Password, +All Hidden

credentials = findHidden(requests.get('https://www.mdimmunet.org/prd-IR/portalInfoManager.do'))
credentials['submit'] = 'Login'

#Grab username and password
#Getpass() used to hide password in terminal
username = raw_input("Immunet username: ")
password = getpass.getpass("Immunet password: ")
print('')

credentials['username'] = username
credentials['password'] = password

#Delete stored username/password
username = ''
password = ''

#Set session with credentials
s = requests.Session()

#Post credentials to login page
s.post('https://www.mdimmunet.org/prd-IR/logon.do', data=credentials)

#Delete username/password in array
credentials = []

#####################################################################################

#SECOND PAGE: MY ACCOUNT PAGE

#Cannot directly follow login screen to the homepage.  Need the homepage to get to search fields.
#Therefore, a connection is made to the profile page that can be accessed because of its lack of a
#secureID present in the URL.  This page provide a link that can be followed to the homepage so 
#long as the correct fields are posted.  These fields are stored in forms []

profilePage = s.get('https://www.mdimmunet.org/prd-IR/selectOrganization.do?pAppId=1&pName=XXX-0')

forms=findHidden(profilePage)
forms['SelectOrganization']='submit'
forms['action']='openApp'
forms['selOrgId']='110113' #Carefirst ID

initalLoginRedirect= s.post('https://www.mdimmunet.org/prd-IR/selectOrganization.do', data=forms)

#####################################################################################

#THIRD PAGE: HOMEPAGE

#Use redirect link from previous post to create connection to homepage screen 
#This is the first screen user sees after successful login

homepage = s.get(initalLoginRedirect.url)	
homeSoup = bs4.BeautifulSoup(homepage.text, "lxml")

if (homeSoup.find('a') == None):
	print('Incorrect username and/or password.\n')
	sys.exit()
	
homeLinks = homeSoup.findAll('a')

#Find url to follow
for link in homeLinks:
	if (link.text == 'Patient Search'):
		secureIdLink = link.get('href')

#Find unique secure ID
defaultURLHead = 'https://www.mdimmunet.org'
secureIdTail = secureIdLink.split('=')[1]
secureId = secureIdTail.split('&')[0]
trueLink = defaultURLHead + secureIdLink

#####################################################################################

#FOURTH PAGE: SEARCH PAGE

#Navigate to advanced search by posting correct fields to advanced search link.
patientSearchForm = s.get(trueLink)

newForms = findHidden(patientSearchForm)
newForms['hAction'] = 'ADVANCEDSEARCH'
newForms['frmWIR'] = 'submit'

patientSearchFormAdvanced = s.post('https://www.mdimmunet.org/prd/!search_ui.matchClient', data=newForms)

#Setting int to keep track of stats
notFound = 0

#####################################################################################

#FIFTH PAGE: ADVANCED SEARCH PAGE + SIXTH PAGE: RESULTS

#This is the start of the actual html scraping process.
#Starts with a simple foreach loop that reads all people retrieved from user input file.
#Each run of the loop will post user search fields, follow the redirect link to the data,
#gather all correct DOM objects, then loop through the objects to collect/write the data.

startTime = datetime.datetime.now()
for index in range(int(indexNumber), len(peopleArray)):
	p = peopleArray[index]
	
	print('Looking up: ' + p.getLastName() + ', ' + p.getFirstName())
	
	#ensure form to be posted is blank for each loop
	pForm = None
	
	pForm = findHidden(patientSearchFormAdvanced)
	pForm['frmWIR'] = 'submit'
	pForm['txtLastName'] = p.getLastName()
	pForm['txtFirstName'] = p.getFirstName()
	pForm['txtBirthDate'] = p.getDateOfBirth()
	pForm['optSexCode'] = p.getGender()

	answer = s.post('https://www.mdimmunet.org/prd/!search_ui.matchClient', data=pForm)
	clientSoup = bs4.BeautifulSoup(answer.text, 'lxml')
	
	#Grabbing the first listed search result
	redirect = clientSoup.find('a', {'id' : 'redirect1'})
	
	#Checking if user was found.  If not found, person is written to second tab of output file.
	if (redirect == None):
		strToWrite = getString(1)
		fileOutputNotFound.write(strToWrite + '\n')
		notFound += 1
	
	#Otherwise, if user is found the link to their data is grabbed and followed. (SIXTH PAGE)
	else:
		#Each user has unique clientID hidden in html.  This logic grabs that ID to use for the final URL
		redirectParameters = redirect['onclick']
		clientId = redirectParameters[21:-3]
		url = 'https://www.mdimmunet.org/prd/wizard_ui.viewClientSchedule?pSecureId=' + secureId + '&pClientId=' + clientId 

		dataRequest = s.get(url)
		dataSoup = bs4.BeautifulSoup(dataRequest.text, 'lxml')
		
		#Unavoidable hardcode to grab the table that contains desired DOM objects
		
		timeout = 0
		while (not dataSoup('table')):
			print('Waiting to reaccess...')
			time.sleep(5)
			timeout += 1
			if (timeout == 12):
				print ('Timeout error. Restart on line ' + index + '\n')
				printStats()
				sys.exit()
			
		dataLinkTable = dataSoup.findAll('table')[18]
		
		#Data being collected is stored in a <tr> tag that alternates class names of evenRow and oddRow.
		#This grabs all these elements and stores them into an array.
		dataLink = dataLinkTable.findAll('tr', {'class' : ['evenRow', 'oddRow']})
		
		print('Record found.')
		
		#Dummy temp set up to ensure large scope.  Used to save implicit data to avoid blank outputs.
		temp = ''
		
		#Looping through all evenRow and oddRow objects
		for data in dataLink:
			#Grab all child elements.  These contain the needed data.
			children = data.findChildren()
			counter = 0
			recordToWrite = getString(0)
			
			for child in children:
				#Need to skip duplicate data stored in <td><a> tags
				if (child.find('a') == None):
					#Checking for implicit data that temp will store (Vaccine Group)
					if (counter == 0):
						if (not (child.text).isspace()):
							temp = child.text
						recordToWrite += (',' + temp.replace(',', ''))
					else:
						#Checking for correct column information to be grabbed
						if (counter != 5 and counter < 7):
							recordToWrite += (',' + (child.text).replace(',', ''))
					counter += 1
				
			answer = recordToWrite.encode('ascii', 'ignore')
			fileOutput.write(answer + '\n')
			
endTime = datetime.datetime.now()

fileOutput.close()
fileOutputNotFound.close()

#Give stats of program
totalPeople = len(peopleArray)
totalHits = totalPeople - notFound
if (totalPeople > 2):
	printStats()

print('\n--------------------OUTPUT--------------------')
print('Files saved: \n' + fileOutputName + '\n' + fileOutputNameNotFound)
print('\n----------------------------------------------\n')
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
