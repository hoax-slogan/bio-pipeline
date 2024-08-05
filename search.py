import requests
from bs4 import BeautifulSoup


def search_geo(term, max_results=5):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={term}&retmax={max_results}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    ids = soup.find_all('Id')

    for id_tag in ids:
        id = id_tag.get_text()
        print(id)
