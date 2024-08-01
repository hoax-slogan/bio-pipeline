from parse_function import parse_xml_metadata
from io import StringIO

def test_parse_xml_metadata():
    xml_metadata = """
                <root>
                <samples>
                    <sample>
                    <id>Sample1</id>
                    <name>Control</name>
                    <value>5.6</value>
                    </sample>
                    <sample>
                    <id>Sample2</id>
                    <name>Test</name>
                    <value>7.8</value>
                    </sample>
                </samples>
                </root>
                """

    expected_output = [
        {'id': 'Sample1', 'name': 'Control', 'value': '5.6'},
        {'id': 'Sample2', 'name': 'Test', 'value': '7.8'}
        ]

    metadata_file = StringIO(xml_metadata)
    result = parse_xml_metadata(metadata_file)

    assert result == expected_output, f"Expected {expected_output}, but got {result}"
