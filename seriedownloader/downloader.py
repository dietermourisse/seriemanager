from http import cookiejar
import urllib.parse
import urllib.request
from utils import getLoginData
import os
import sys

downloaddir = '/Users/watchtower/Downloads'

class rapidGatorConnection:

	def __init__(self):
		self.cj = cookiejar.CookieJar()
		self.opener = None
		self.chunksize = 16 * 1024
		if not os.path.isdir(downloaddir):
			os.mkdir(downloaddir)

	def getName():
		return 'rapidgator'

	def connect(self):
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
		login_data = getLoginData('rapidgator')
		url = 'https://rapidgator.net/auth/login'
		values = {
				'LoginForm[email]': login_data[0],
				'LoginForm[password]': login_data[1],
				'LoginForm[rememberMe]': 0}
		postdata = urllib.parse.urlencode(values)
		postdata = postdata.encode('utf-8')
		req = self.opener.open(url, data=postdata)

	def download(self, link):
		if not self.opener:
			self.connect()
		print(link)
		req = self.opener.open(link)
		data = req.read().decode('utf-8').split('\n')
		link = list(filter(lambda x : 'var premium_download_link' in x, data))[0].split("'")[1]
		req = self.opener.open(link, timeout=5.0)
		info = req.info()
		filename = None
		size = None
		if 'Content-Disposition' in info.keys():
			filename = info['Content-Disposition'].split('"')[1]
		if 'Content-Length' in info.keys():
			size = int(info['Content-Length'])

		done = 0
		procent = float(0)
		print(filename, size)
		if filename and size and not os.path.exists(os.path.join(downloaddir, filename)):
			fp = open(os.path.join(downloaddir, filename), 'wb')
			print('Downloading')
			chunk = req.read(self.chunksize)
			while chunk:
				done += self.chunksize
				if round(100*done/size,2) > procent:
					procent = round(100*done/size,2)
					sys.stdout.write(' {}%\r'.format(procent))
					sys.stdout.flush()
				fp.write(chunk)
				chunk = req.read(self.chunksize)
			fp.close()
		return (filename, size)

	def download_links(self, links):
		locations = []
		connection = None
		for link in links:
			location = self.download(link)
			locations.append(location)
		return locations

class netLoadConnection:

	def __init__(self):
		self.cj = cookiejar.CookieJar()
		self.opener = None
		self.chunksize = 16 * 1024
		#check if tempdir available
		if not os.path.isdir(downloaddir):
			os.mkdir(downloaddir)

	def getName():
		return 'netload'

	def connect(self):
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
		login_data = getLoginData('netload')
		url = 'http://netload.in/index.php'
		values = {
			'txtuser' : login_data[0],
			'txtpass' : login_data[1],
			'txtcheck' : 'login',
			'txtlogin': 'Login'
		}
		postdata = urllib.parse.urlencode(values)
		postdata = postdata.encode('utf-8')
		req = self.opener.open(url, data=postdata)

	def download(self, link):
		if not self.opener:
			self.connect()
		req = self.opener.open(link, timeout = 5.0)
		info = req.info()
		filename = None
		size = None
		if 'Content-Disposition' in info.keys():
			filename = info['Content-Disposition'].split('"')[1]
		if 'Content-Length' in info.keys():
			size = int(info['Content-Length'])
			print(size)

		done = 0
		procent = float(0)
		print(filename, size)
		if filename and size and not os.path.exists(os.path.join(downloaddir, filename)):
			fp = open(os.path.join(downloaddir, filename), 'wb')
			print('Downloading')
			chunk = req.read(self.chunksize)
			while chunk:
				done += self.chunksize
				if round(100*done/size,2) > procent:
					procent = round(100*done/size,2)
					sys.stdout.write(' {}%\r'.format(procent))
					sys.stdout.flush()
				fp.write(chunk)
				chunk = req.read(self.chunksize)
			fp.close()
		return (filename, size)

class Downloader:

	def __init__(self):
		self.connections = dict()

	def getNewConnection(self, connectiontype):
		connection = None
		if connectiontype == 'netload':
			connection =  netLoadConnection()
		return connection

	def get_connection(self, link):
		linktype = None
		if 'netload.in' in link:
			linktype = 'netload'

		if not linktype in self.connections:
			self.connections[linktype] = self.getNewConnection(linktype)
			return self.connections[linktype]
		else:
			return self.connections[linktype]

	def download_link(self, link):
		connection = self.get_connection(link)
		location = connection.download(link)
		return location

	def download_links(self, links):
		locations = []
		connection = None
		for link in links:
			location = self.download_link(link)
			locations.append(location)
		return locations



if __name__ == '__main__':
	print('Running in test mode')
	connection = rapidGatorConnection()
	for link in open('links.txt', 'r'):
		try:
			location = connection.download(link)
			print(location)
		except:
			print('ERROR WITH LINK: {}'.format(link))	
	#connection.download_links(['http://rapidgator.net/file/c982d8f7d98236618bcca99397940ed9/The.Legend.of.Korra.S03E11.The.Ultimatum.720p.WEBRip.x264.AAC.mp4.html'])

