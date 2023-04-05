from base64 import b64encode
from re import sub

def decode_image(movie):
    return b64encode(movie.image).decode('ascii')

def remove_special_chars(chars):
    special_char_regex = r'[^a-zA-Z0-9\s]+'

    return sub(special_char_regex, '', chars)
