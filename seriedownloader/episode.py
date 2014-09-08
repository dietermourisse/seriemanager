from downloader import Downloader

def addNewEpisode(show, season, episode):
	links = []
	title = ['']*len(links)
	for i in range(len(links)):
		link = links[i]
		title = titles[i]
		filename = '{0} - s{1:0>2}e{2:0>2} - {3}'.format(show, season, episode, title)
	

def download_episode(self, show, season, episode, links):
	downloader = Downloader()
	locations = donwloader.download_links(links):
	return locations

	def download_episode(self, toDownload, t):
		links = {(a, b, c, d) : e for a, b, c, d, e in toDownload}
		locations = download_links(links, t)