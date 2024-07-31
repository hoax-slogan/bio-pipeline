from parse_function import parse_json_metadata

def test_parse_json_metadata():
    json_metadata = '{"samples": [{"id": "Sample1" }, { "id": "Sample2" }]}'
    expected_output = {
        'samples': [{'id': 'Sample1'}, {'id': 'Sample2'}]
    }

    result = parse_json_metadata(json_metadata)

    assert result == expected_output, f"Expected {expected_output}, but got {result}"
