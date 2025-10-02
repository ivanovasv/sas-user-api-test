import json


def load_payload(payload_file):
    """
        Load a JSON payload from the 'payloads/' folder.
        :param payload_file: Name of the JSON file to load
        :return: Dictionary with JSON content or None
    """
    if not payload_file:
        return None
    with open(f"payloads/{payload_file}", "r") as f:
        return json.load(f)


def correct_json_values(value):
    """
        Convert string values from table to proper Python types.
        Handles booleans, nulls, integers and floats automatically.
        :param value: Value from the table as string
        :return: Properly typed Python value
    """
    if isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        elif value.lower() == "null":
            return None
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            return value
    return value