loginfile = 'login_data.txt'

def getLoginData(service):
	f = open(loginfile)
	data = eval(f.read())[service]
	f.close()
	return data

def grep(lines, expression):
	import re
	results = []
	for line in lines:
		if re.search(expression, line):
			results.append(line)
	return results