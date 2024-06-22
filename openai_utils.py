import json
from typing import Union
from openai.types.chat import ChatCompletion


def extract_message_from_openai_message(response: ChatCompletion) -> Union[str, None]:
    """
    Extract the message from the ChatCompletion response object.

    Args:
        response (ChatCompletion): The response object returned by the OpenAI API.

    Returns:
        str: The message extracted from the response.
    """
    if response.choices:
        message = response.choices[0].message.content
        return message
    else:
        return None
