import json
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree


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


def parse_geo_metadata_text(metadata_text):
    format_type = detect_format(metadata_text)

    if format_type == 'json':
        return parse_json_metadata(metadata_text)
    elif format_type == 'xml':
        return parse_xml_metadata(metadata_text)
    elif format_type == 'html':
        return parse_html_metadata(metadata_text)
    else:
        return parse_text_metadata(metadata_text)


def parse_json_metadata(metadata_text):
    metadata = json.loads(metadata_text)
    return metadata


def parse_xml_metadata(metadata_text):
    metadata = etree.parse(metadata_text)
    etree.tostring(metadata.getroot())


def parse_html_metadata(metadata_text):
    pass


def parse_text_metadata(metadata_text):
    pass
