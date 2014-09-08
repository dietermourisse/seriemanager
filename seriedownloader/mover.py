import os
import os.path

standardlocation = '/Users/watchtower/Downloads'
def getFiles(filelocation = standardlocation):
	files = [f for f in os.listdir(filelocation)]
	files = filter(lambda x: not x.startswith('.'), files)
	result = []
	for current in files:
		print(current)
		if os.path.isdir(os.path.join(filelocation, current)):
			answer = input('Move files in directory {}: '.format(current))
			if answer == 'y':
				result += getFiles(os.path.join(filelocation, current))
		else:
			proceed = False
			while not proceed:
				answer = input('Move file: ')
				if answer == 'y':
					proceed = True
					serie = input('Serie: ')
					season = ''
					episode = ''
					if serie != '':
						season = input('Season: ')
						episode = input('Episode: ')
						result.append((serie, season, episode, os.path.join(filelocation, current)))
				elif answer == 'n':
					proceed = True
	return result

def move(files, destination = '/Volumes/series'):
	for videofile in files:
		serie, season, episode, source = videofile
		episode = episode.zfill(2)
		extension = source.split('.')[-1]
		directory = os.path.join(destination, serie, 'Season {}'.format(season))
		season.zfill(2)
		if not os.path.exists(directory):
			os.makedirs(directory)
		destinationfile = os.path.join(directory, '{} - s{}e{} - .{}'.format(serie, season, episode, extension))
		os.system('rsync --progress "{}" "{}"'.format(source, destinationfile))

if __name__ == '__main__':
	files = getFiles()
	move(files)


