import logging
from fetch import fetch_geo_data
from search import search_geo
from parse import parse_geo_data


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    search_term = input("Enter the search term for tissue or cell type of interest: ")
    print()
    search_geo(search_term)

    geo_ids = input("\nEnter UID's here (seperate by comma): ")
    fetch_geo_data(geo_ids)

if __name__ == "__main__":
    main()
