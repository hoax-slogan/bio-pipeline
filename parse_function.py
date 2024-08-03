import logging
import json
import pandas as pd
from collections import defaultdict
from lxml import etree
from typing import Any, Dict, List,  Optional, Union


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


def parse_json_metadata(metadata_text: Union[str, bytes]) -> Optional[Union[Dict[str, Any], List[Any]]]:
    """
    Parses JSON metadata from a given text or file-like object.

    Args:
        metadata_text (str or bytes): JSON content to be parsed.

    Returns:
        Optional[Union[Dict[str, Any], List[Any]]]: A parsed JSON object,
        which can be a dictionary or a list, or None is parsing fails.
    """
    try:
        metadata = json.loads(metadata_text)
        # all_keys = set()

        # # Collect all unique keys iteratively
        # stack = [metadata]
        # while stack:
        #     current = stack.pop()
        #     if isinstance(current, dict):
        #         for key, value in current.items():
        #             all_keys.add(key)
        #             if isinstance(value, (dict, list)):
        #                 stack.append(value)
        #     elif isinstance(current, list):
        #         stack.extend(current)

        # # Fill missing keys and replace empty strings iteratively
        # stack = [metadata]
        # while stack:
        #     current = stack.pop()
        #     if isinstance(current, dict):
        #         for key in all_keys:
        #             if key not in current:
        #                 current[key] = None
        #         for key, value in current.items():
        #             if isinstance(value, str) and value == "":
        #                 current[key] = None
        #             elif isinstance(value, (dict, list)):
        #                 stack.append(value)
        #     elif isinstance(current, list):
        #         for item in current:
        #             stack.append(item)

        # return metadata

        if isinstance(metadata, dict):
            for key, value in metadata.items():
                if isinstance(value, str) and value == "":
                    metadata[key] = None
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            for k, v in item.items():
                                if isinstance(v, str) and v == "":
                                    item[k] = None
                        elif isinstance(item, str) and item == "":
                            item = None

        elif isinstance(metadata, list):
            for item in metadata:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, str) and value == "":
                            item[key] = None
                elif isinstance(item, str) and item == "":
                    item = None

        return metadata
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


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

        # Iterate through all elements in the XML
        for element in root.iter():
            if len(element) > 0:
                sample_data = {}
                for child in element:
                    if child.text and child.text.strip():
                        sample_data[child.tag] = child.text
                    else:
                        sample_data[child.tag] = None
                # Only add non-empty sample_data dictionaries
                if any(sample_data.values()):
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
