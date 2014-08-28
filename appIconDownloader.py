import urllib2
import json
import os
import shutil
import thread

downloadCount = 0
totalDownloads = 0

# Download a single file
def downloadFile(url, destination):
	global downloadCount
	
	f = open(destination, 'wb')
	f.write(urllib2.urlopen(url).read())
	f.close()

	downloadMessage = 'Completed download ' + str(totalDownloads - downloadCount + 1) + '/' + str(totalDownloads)

	downloadCount -= 1

	print(downloadMessage)

# Icon downloading (multithreaded implementation)
def downloadIcons(searchTerm, results, verbosity):
	global downloadCount

	if verbosity > 0:
		print('Beginning download of ' + str(results) + ' results for search term "' + searchTerm + '"')

	if verbosity > 1:
		print('Sending HTTP request')

	requestString = 'https://itunes.apple.com/search?term=' + searchTerm + '&country=us&entity=software&media=software&limit=' + str(results)
	response = urllib2.urlopen(requestString).read()

	if verbosity > 1:
		print('Received HTTP response')
		print('Parsing into JSON')

	responseJSON = json.loads(response)
	resultCount = responseJSON['resultCount']

	if verbosity > 1:
		print('Received ' + str(resultCount) + ' results')

	for i in range(resultCount):
		appDict = responseJSON['results'][i]
		appName = appDict['trackName']
		appIcon60 = appDict['artworkUrl60']
		appIcon512 = appDict['artworkUrl512']
		appIcon60Ext = appIcon60[appIcon60.rindex('.'):]
		appIcon512Ext = appIcon512[appIcon512.rindex('.'):]

		appName = appName.replace('/', ' ')

		if verbosity > 0:
			print('Downloading App "' + searchTerm + '" ' + str(i + 1) + '/' + str(resultCount))

		if verbosity > 1:
			print('\tName: ' + appName)
			print('\tIcon 512x512: ' + appIcon512[appIcon512.rindex('/') + 1:])

		targetDir = 'Icons/' + searchTerm + '/'

		downloadCount += 1

		thread.start_new_thread(downloadFile, ((appIcon512, targetDir + appName + '512x512' + appIcon512Ext)))

		if verbosity > 1:
			print ('\t\tDownloaded!\n')

# Main function
if __name__ == '__main__':
	if not os.path.isdir('Icons'):
		os.mkdir('Icons')

	while (True):
		searchTerm = raw_input('Please enter the search terms seperated by commas (! to exit): ')
		if searchTerm == '!':
			break

		searchTermList = searchTerm.split(',')

		threadedTerms = []

		for term in searchTermList:
			targetDir = 'Icons/' + term

			if os.path.isdir(targetDir):
				userResponse = raw_input('Icons for search term "' + term + '" have already been downloaded... Redownload (y/n)? ')
				if userResponse == 'n':
					continue

				shutil.rmtree(targetDir)

			threadedTerms.append(term)

			os.mkdir(targetDir)

		for term in threadedTerms:
			totalDownloads += 200
			thread.start_new_thread(downloadIcons, (term, 200, 0))

		wait = raw_input()

		