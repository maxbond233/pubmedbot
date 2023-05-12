import requests

from bs4 import BeautifulSoup
from url_manager import UrlManager

class SearchPageCrawler():
	'''
	This class is used to crawl the search page.
	'''

	def __init__(self, term):
		self.root_url = "https://pubmed.ncbi.nlm.nih.gov/"
		self.headers = {'user-agent': 
						'''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'''}
		self.term = term

		# get results
		self.article_urls = UrlManager()
		self.total_pages = 0
	
	def access_search_page(self, page = 1):
		'''
		This function is used to access the search page. returns a BeautifulSoup object.
        '''

		params = {'term': self.term, 'page': page}

		r = requests.get(self.root_url, params=params, headers=self.headers)

		if r.status_code!= 200:
			raise Exception()
		html_doc = r.text
		soup = BeautifulSoup(html_doc, "html.parser")
		return soup


	def get_total_pages(self):
		'''
		This function is used to get the results total page numbers. returns a integers.
		'''

		soup = self.access_search_page(page = 1)
		total_pages = soup.find('div', {'class': 'page-number-wrapper'}).find('label', {'class': 'of-total-pages'}).text
		self.total_pages = int(total_pages[2:].replace(',', ''))


	def get_article_urls(self):
		'''
        This function is used to get the article urls.
		The urls are stored in the UrlManager class.
        '''

		for i in range(1, self.total_pages + 1):
			soup = self.access_search_page(page = i)
			articles = soup.find_all('a', {'class': 'docsum-title'})
			for article in articles:
				href = article.get('href')
				if href is None: continue
				href = self.root_url + href
				self.article_urls.add_new_url(href)

	def get_article_basic_info(self):
		'''
		This function is used to get the article basic info.
		'''

		for i in range(1, self.total_pages + 1):
			soup = self.access_search_page(page = i)

			# get the basic info from the docsum-title
			articles = soup.find_all('div', {'class': 'docsum-content'})
			title = articles.find('a', {'class': 'docsum-title'}).text
			authors = soup.find('div', {'class': 'docsum-authors'}).text
			pub_date = soup.find('div', {'class': 'docsum-pubdate'}).text
			doi = soup.find('div', {'class': 'docsum-doi'}).text

if __name__ == '__main__':
	search_page_crawler = SearchPageCrawler(term='scRNA')
	search_page_crawler.get_total_pages()
	print(search_page_crawler.total_pages)
	search_page_crawler.get_article_urls()

