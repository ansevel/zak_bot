import re


def get_purchase_num_form_message(message_text: str) -> str:
    pattern = r'^Номер: (\d+)'
    text_match = re.search(pattern, message_text)
    return text_match.group(1)
