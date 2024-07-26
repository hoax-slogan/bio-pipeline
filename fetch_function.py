import requests


def fetch_geo_data(id):
    url_data = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id={id}"
    try:
        response_data = requests.get(url_data)
        raw_data = response_data.text
        print(raw_data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
    except Exception as err:
        print(f"An error occured: {err}")


def fetch_geo_metadata(id):
    url_metadata = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id}&targ=self&form=text&view=full"
    response_metadata = requests.get(url_metadata)
    # metadata = parse_geo_metadata(response_metadata)
    # print(metadata)
