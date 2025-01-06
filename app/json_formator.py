from typing import Any, Dict

def format_response(data: Dict[str, Any], message: str = "Request processed successfully") -> Dict[str, Any]:
    """
    Formats a response in a consistent structure.

    Args:
        data (Dict[str, Any]): The main data to include in the response.
        message (str): A custom message for the response. Defaults to a success message.

    Returns:
        Dict[str, Any]: A dictionary representing the formatted response.
    """
    return {
        "data": data,
        "message": message,
    }
