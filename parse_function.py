import json
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree


def detect_format(metadata_text):
    try:
        json.loads(metadata_text)
        return 'json'
    except json.JSONDecodeError:
        pass
    
    try:
        etree.fromstring(metadata_text)
        return 'xml'
    except etree.XMLSyntaxError:
        pass

    if metadata_text.strip().startswith('<'):
        return 'html'

    return 'text'


def parse_geo_data(raw_data):
    lines = raw_data.split('\n')
    data_dict = {'Gene': [], 'Value': []}

    for line in lines:
        if line.startswith('!') or not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) > 1:
            data_dict['Gene'].append(parts[0])
            data_dict['Value'].append(parts[1:])

    df = pd.DataFrame(data_dict)
    df.set_index('Gene', inplace=True)
    return df


def parse_geo_metadata(metadata):
    soup = BeautifulSoup(metadata, 'html.parser')
    meta_dict = {}

    for line in metadata.splitlines():
        if line.startswith("!Sample_title"):
            sample_titles = line.split('\t')[1:]
            meta_dict['SampleID'] = sample_titles
    return meta_dict
