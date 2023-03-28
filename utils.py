from  base64 import b64encode

def decode_image(image):
    return b64encode(image.image).decode('ascii')
