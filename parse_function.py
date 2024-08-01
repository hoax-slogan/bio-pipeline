import logging
import json
import pandas as pd
from collections import defaultdict
from lxml import etree
from typing import List, Dict, Union, Optional


logger = logging.getLogger(__name__)


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


def parse_xml_metadata(metadata_text: Union[str, bytes]) -> Optional[List[Dict[str, Optional[str]]]]:
    """
    Parses XML metadata from a given text or file-like object.

    Args:
        metadata_text (str or bytes): XML content to be parsed.

    Returns:
        List[Dict[str, Optional[str]]]: A list of dictionaries
        containing sample data, or None if parsing fails.
    """
    try:

        if hasattr(metadata_text, 'read'):
            metadata = etree.parse(metadata_text)
        else:
            metadata = etree.fromstring(metadata_text)

        root = metadata.getroot()
        samples = []

        for sample in root.findall('.//sample'):
            sample_data = defaultdict(lambda: None)
            for child in sample:
                sample_data[child.tag] = child.text
            samples.append(dict(sample_data))

        return samples

    except etree.XMLSyntaxError as e:
        logger.error(f"XML Syntax Error: {e}")
    except etree.ParseError as e:
        logger.error(f"Parse error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


def parse_html_metadata(metadata_text):
    pass


def parse_text_metadata(metadata_text):
    pass
