from behave import step
from jsonpath_ng import parse
from common.payload_builder import *
from common.utils import get_value_from_context


@step('API: Send {method} {endpoint} request {condition} payload')
@step('API: Send {method} {endpoint} request {condition} payload from {path}')
def api_send_request(context, method, endpoint, condition, path=None):
    """
    Send an HTTP request to a specified endpoint with or without a payload.
    Optionally, load payload from a file path if provided.

    :param context: Behave context
    :param method: HTTP method: GET / POST / PUT / DELETE
    :param endpoint: API endpoint
    :param condition: with or without
    :param path: optional payload file name inside the 'payloads/' folder

    Example usage:
        * API: Send GET /users request without payload
        * API: Send POST /users request with payload from create_user.json
    """

    assert condition in ["with", "without"], "Condition must be 'with' or 'without'"

    endpoint = get_value_from_context(context, endpoint)
    payload = None

    if condition == "with":
        # Load payload from file or context if available
        if path:
            payload = load_payload(path)
        else:
            payload = getattr(context, "payload", None)

        if payload is None:
            raise ValueError("Payload expected but not found.")

    # Send request using shared api_client
    context.response = context.api_client.send_request(
        method=method,
        endpoint=endpoint,
        payload=payload
    )


@step('API: Prepare payload for {payload_file}')
def prepare_payload_for_api(context, payload_file):
    """
    Load payload from a file and update its values using JSONPath.

    :param context: Behave context
    :param payload_file: filename of JSON in the 'payloads/' folder

    Example:
        * API: Prepare payload for create_user.json
            | jsonPath   | value     |
            | $.username | test_user |
    """
    payload = load_payload(payload_file)
    if payload is None:
        raise ValueError(f"Payload file '{payload_file}' not found or empty")

    if context.table:
        for row in context.table:
            json_path = row["jsonPath"]
            value = correct_json_values(row["value"])

            expr = parse(json_path)
            matches = expr.find(payload)

            if not matches:
                raise KeyError(f"No match found for JSONPath: {json_path}")

            for match in matches:
                match.path.update(payload, value)

    context.payload = payload

    print("Prepared Payload:")
    print(json.dumps(payload, indent=2))


@step('API: response {condition} have api status code {code}')
def assert_api_status_code(context, condition, code):
    """
    Assert API status code is equal to the specified code

    :param context: Behave context
    :param condition: "should" or "should not"
    :param code: 200 /201 / 400

    Example:
        * API: response should have api status code 200
    """

    assert condition in ["should", "should not"], "Condition must be 'should' or 'should not'"

    response = getattr(context, 'response', None)
    actual_code = context.response.status_code
    expected_code = int(code)

    if condition == "should":
        assert actual_code == expected_code, (
            "Received status code does not match expected code."
            f"\n\tExpected:\t{expected_code}\n\tReceived:\t{actual_code}"
            f"\n\tResponse text:\t{response.text}")
    else:
        assert actual_code != expected_code, (
            f"\nUnexpected match:"
            f"\n\tReceived and Expected status code are equal to {expected_code}")


@step('API: Response {condition} have values')
def verify_api_response_values(context, condition):
    """
    Verify API response values by JSONPath against expected values from the table.

    :param context: Behave context
    :param condition: "should" or "should not"

    Example:
        Then API: Response should/should not have values
            | jsonPath   | value |
            | $.username | Test  |
            | $.id       | 1     |
    """
    assert condition in ["should", "should not"], "Condition must be 'should' or 'should not'"

    response = getattr(context, "response", None)
    assert response is not None, "No API response found in context"

    try:
        resp_json = response.json()
    except Exception:
        raise AssertionError("Response is not JSON:\n" + response.text)

    for row in context.table:
        json_path = row["jsonPath"]
        expected_raw = row["value"]

        expected_from_context = get_value_from_context(context, expected_raw)

        expected_value = str(correct_json_values(expected_from_context))

        expr = parse(json_path)
        matches = [str(match.value) for match in expr.find(resp_json)]

        if condition == "should":
            assert matches, f"Expected value at {json_path}, but nothing was found."
            assert expected_value in matches, (
                f"\nExpected value {expected_value} not found at {json_path}. "
                f"\nActual values: {matches}")
        else:
            if expected_value in matches:
                raise AssertionError(
                    f"\nUnexpected value {expected_value} found at {json_path}. "
                    f"\nActual values: {matches}")

    print("Response values verified successfully.")


@step('API: Save values from JSON response')
def save_multiple_values_from_response(context):
    """
    Save multiple values from response to context using JSONPath.

    Example:
        * API: Save values from JSON response
            | jsonPath | varName  |
            | $.id     | user_id  |
            | $.name   | name     |
    """
    response = getattr(context, "response", None)
    assert response is not None, "No response object found in context"

    try:
        resp_json = response.json()
    except Exception:
        raise AssertionError("Response is not valid JSON:\n" + response.text)

    for row in context.table:
        json_path = row["jsonPath"]
        var_name = row["varName"]

        expr = parse(json_path)
        matches = [match.value for match in expr.find(resp_json)]

        assert matches, f"No match found for JSONPath: {json_path}"
        if len(matches) > 1:
            raise ValueError(f"Multiple values found at {json_path}. Use a more specific path.")

        value = matches[0]
        setattr(context, var_name, value)
        print(f"Saved to context.{var_name} = {value}")