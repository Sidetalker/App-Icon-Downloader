import urllib2
import json
import os
import shutil
import thread

# Download a single file
def downloadFile(url, destination, message):
	f = open(destination, 'wb')
	f.write(urllib2.urlopen(url).read())
	f.close()

	print(message)

# Icon downloading (multithreaded implementation)
def downloadIcons(searchTerm, results, verbosity):
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

		downloadMessage = 'Completed download ' + str(i + 1) + '/' + str(results) + ' for search term "' + searchTerm + '"'

		thread.start_new_thread(downloadFile, ((appIcon512, targetDir + appName + '512x512' + appIcon512Ext, downloadMessage)))

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

			targetDir += '/'

		for term in threadedTerms:
			thread.start_new_thread(downloadIcons, (term, 200, 0))

		wait = raw_input()

		