import re
import requests
from bs4 import BeautifulSoup
from utils import url_manager

# get the pubmed root page

term = "scatac-seq"
root_url = "https://pubmed.ncbi.nlm.nih.gov/?term=%s" %term

r = requests.get(root_url)
if r.status_code != 200: 
    raise Exception()

html_doc = r.text
soup = BeautifulSoup(html_doc, "html.parser")

# get all the articles
arts = soup.find_all("a", class_="docsum-title")

# a new UrlManager is used to keep track of all the new urls
urls = url_manager.UrlManager()
for art in arts:
    href = art.get('href')
    if href is None: continue
    href = "https://pubmed.ncbi.nlm.nih.gov" + href
    urls.add_new_url(href)


fout = open("craw_all_pages.txt", "w")
# get information in each article
while urls.has_new_url(): 
    curr_url = urls.get_url()
    r = requests.get(curr_url, timeout=3)
    if r.status_code!= 200: 
        print("ERROR, return status code is not 200:", curr_url)
        continue
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('main', class_='article-details')

    pmid = content.find('strong', class_='PumMed ID').get_text()
    title = content.find('h1', class_='article-title').get_text()

    fout.write("%s\t%s\n" % (pmid, title))
    fout.flush()

fout.close()


# while urls.has_new_url(): 
#     curr_url = urls.get_url()
#     r = requests.get(curr_url, timeout=3)
#     if r.status_code != 200: 
#         print("ERROR, return status code is not 200:", curr_url)
#         continue
#     soup = BeautifulSoup(r.text, 'html.parser')
#     title = soup.title.string

#     fout.write("%s\t%s\n" % (curr_url, title))
#     fout.flush()
#     print("success: %s, %s, %d" % (curr_url, title, len(urls.new_urls)))

#     links = soup.find_all('a')
#     for link in links:
#         href = link.get('href')
#         if href is None: continue
#         pattern = r'^http://www.crazyant.net/\d+.html$'
#         if re.match(pattern, href):
#             urls.add_new_url(href)

