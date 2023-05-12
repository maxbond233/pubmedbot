import re
import requests
from bs4 import BeautifulSoup
from utils import url_manager

# set access headers

headers = {'user-agent': 
               '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'''}

# get the pubmed root page

def access_pubmed_root_page(headers=headers):
    root_url = "https://pubmed.ncbi.nlm.nih.gov/"


def access_pubmed_search_page(term):
    params = {'term': term, 'page': '1'}

    headers = {'user-agent': 
               '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'''}
    
    root_url = "https://pubmed.ncbi.nlm.nih.gov/"

    r = requests.get(root_url, params=params, headers=headers)

    print(r.status_code)
    if r.status_code!= 200: 
        raise Exception()

access_pubmed_search_page("human")


