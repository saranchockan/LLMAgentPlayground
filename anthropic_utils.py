from anthropic.types import Message


def extract_text_from_anthropic_message(message: Message):
    """
    Extracts and concatenates all text content from a Message object.

    Args:
        message (Message): A Message object returned by the Anthropic Python SDK.

    Returns:
        str: A string containing all the text content from the Message object.
    """
    text = ""
    for content_item in message.content:
        if content_item.type == "text":
            text += content_item.text
    return text
