from fetch_function import fetch_geo_data
from search_function import search_geo
from parse_function import parse_geo_data


def main():
    search_term = input("Enter the search term for tissue or cell type of interest: ")
    print()
    search_geo(search_term)

    geo_ids = input("\nEnter UID's here (seperate by comma): ")
    fetch_geo_data(geo_ids)
    geo_dfs = []

    # for geo_id in geo_ids:
        # geo_df = parse_geo_data_and_metadata(geo_id)
        # geo_dfs.append(geo_df)

    print(geo_dfs.head())




if __name__ == "__main__":
    main()
