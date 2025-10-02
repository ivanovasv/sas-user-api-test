import re


def get_value_from_context(context, value):
    """
    If the value is 'context.var_name', returns value from Behave context.
    Otherwise returns the value unchanged.
    """
    if isinstance(value, str):
        matches = re.findall(r"context\.(\w+)", value)
        for var in matches:
            context_value = getattr(context, var, f"context.{var}")
            value = value.replace(f"context.{var}", str(context_value))
    return value