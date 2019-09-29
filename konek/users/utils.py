from konek import app
import secrets, os
from PIL import Image


def save_picture(image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image.filename)
    # create salt filename
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imgs', picture_name)
    image.save(picture_path)

    output_size = (125, 125)
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name