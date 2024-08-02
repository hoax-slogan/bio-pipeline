from parse_function import parse_xml_metadata
from io import StringIO

def test_nice_xml_metadata():
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

    metadata_content = StringIO(xml_metadata)
    result = parse_xml_metadata(metadata_content)

    assert result == expected_output, f"Expected {expected_output}, but got {result}"


def test_malformed_xml_metadata():
    malformed_xml = """
                    <root>
                        <samples>
                            <sample>
                                <id>Sample1</id>
                                <name>Control<name> <!-- Missing closing tag for <name> -->
                                <value>5.6</value>
                            </sample>
                            <sample>
                                <id>Sample2<id> <!-- Missing closing tag for <id> -->
                                <name>Test</name>
                                <value>7.8</value>
                            </sample>
                            <sample>
                                <id>Sample3</id>
                                <name>Invalid & Name</name> <!-- Invalid character & in the name -->
                                <value>8.9<value> <!-- Missing closing tag for <value> -->
                            </sample>
                        </samples>
                    </root>
                """

    metadata_content = StringIO(malformed_xml)
    result = parse_xml_metadata(metadata_content)

    assert result is None, f"Expected None, but got {result}"


def test_empty_xml_metadata():
    empty_xml = ""

    metadata_content = empty_xml
    result = parse_xml_metadata(metadata_content)

    assert result is None, f"Expected None, but got {result}"


def test_partial_xml_metadata():
    partial_xml = """
                <root>
                <samples>
                    <sample>
                    <id>Sample1</id>
                    </sample>
                </samples>
                </root>
                """

    expected_output = [
        {'id': 'Sample1'}
    ]

    metadata_content = StringIO(partial_xml)
    result = parse_xml_metadata(metadata_content)

    assert result == expected_output, f"Expected {expected_output}, but got {result}"
