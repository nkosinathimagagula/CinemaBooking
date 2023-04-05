from base64 import b64encode
from re import sub

def decode_image(image):
    return b64encode(image.image).decode('ascii')

def remove_special_chars(chars):
    special_char_regex = r'[^a-zA-Z0-9\s]+'

    return sub(special_char_regex, '', chars)
    