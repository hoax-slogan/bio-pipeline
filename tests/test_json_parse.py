from parse_function import parse_json_metadata


def test_nice_json_metadata():
    json_metadata = '{"samples": [{"id": "Sample1" }, { "id": "Sample2" }]}'

    expected_output = {
        'samples': [{'id': 'Sample1'}, {'id': 'Sample2'}]
    }

    result = parse_json_metadata(json_metadata)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"


def test_malformed_json_metadata():
    malformed_json = """
                        {
                            'samples': [
                                {'id': 'Sample1', 'name': 'Control', 'value': 5.6}
                                {'id': 'Sample2', 'name': 'Test', 'value': 7.8},
                            ]
                        }
                    """

    expected_output = None

    result = parse_json_metadata(malformed_json)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"


def test_empty_json_metadata():
    empty_json = "{}"

    expected_output = {}

    result = parse_json_metadata(empty_json)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"


def test_partial_json_metadata():
    partial_json =  """
                        {
                        "samples": [
                            {"id": "Sample1", "name": "Control", "value": 5.6},
                            {"id": "Sample2"}
                        ]
                        }
                    """

    expected_outcome = {
        "samples": [
            {"id": "Sample1", "name": "Control", "value": 5.6},
            {"id": "Sample2", "name": None, "value": None}
        ]
    }

    result = parse_json_metadata(partial_json)
    assert result == expected_outcome, f"Expected {expected_outcome}, but got {result}"
