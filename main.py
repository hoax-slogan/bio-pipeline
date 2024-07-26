from search_function import search_geo
from fetch_function import fetch_geo_data


def main():
    search_term = input("Enter the search term for tissue or cell type of interest: ")
    search_geo(search_term)

    geo_id = input("Enter UID's here (seperate by comma): ")
    fetch_geo_data(geo_id)


if __name__ == "__main__":
    main()
