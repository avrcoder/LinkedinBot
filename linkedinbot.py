from bs4 import BeautifulSoup
import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def getpeoplelinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if 'profile/view?id=' in url:
				links.append(url)
	return links

def getjobprofiles(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if '/jobs' in url:
				links.append(url)
	return links

def getID(url):
	pUrl = urlparse.urlparse(url)
	return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
	visited = {}
	pList = []
	count = 0
	while True:
		#sleep to make sure everything loads
		#use random function to eliminate the suspition of being caught
		time.sleep(random.uniform(4,7))
		page = BeautifulSoup(browser.page_source)
		people = getpeoplelinks(page)
		if people:
			for person in people:
				ID = getID(person)
				if ID not in visited:
					pList.append(person)
					visited[ID] = 1
		if pList:
			person = pList.pop()
			browser.get(person)
			count+=1
		else:
			jobs = getjobprofiles(page)
			if jobs:
				job = random.choice(jobs)
				root = 'http://www.linkedin.com'
				roots = 'http://www.linkedin.com'
				if job not in root or job not in roots:
					job = 'http://www.linkedin.com' + job
				browser.get(job)
			else:
				print "I'm lost exiting"
				break
		print browser.title + "visited. No of people visited = "+str(count)+". No of people to be visited = "+str(len(pList))+"."

def main():
	# parser = argparse.ArgumentParser()
	# parser.add_argument("email", help = "linkedin email")
	# parser.add_argument("password", help = "linkedin password")
	# args = parser.parse_args()
	email = raw_input("Enter your mail id")
	password = raw_input("Enter the password")

	browser = webdriver.Firefox()
	browser.get("http://linkedin.com/uas/login")

	emailElement = browser.find_element_by_id("session_key-login")
	emailElement.send_keys(email)
	passElement = browser.find_element_by_id("session_password-login")
	passElement.send_keys(password)
	passElement.submit()

	os.system('cls')
	print "Successfully logged in"
	ViewBot(browser)
	browser.close()

if __name__ == '__main__':
	main()