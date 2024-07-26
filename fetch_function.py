import requests


def fetch_geo_data(id):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id={id}"
    response = requests.get(url)
    print(response.text)
