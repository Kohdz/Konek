from konek import app
import secrets, os
from PIL import Image


def save_picture(image):
    random_hex = secrets.token_hex(8)
    # split image filename
    _, f_ext = os.path.splitext(image.filename)
    # create modified name for picture file
    picture_name = random_hex + f_ext
    # create absolute path for new picture image
    picture_path = os.path.join(app.root_path, 'static/imgs', picture_name)
    # save the image to the picture_path we created
    image.save(picture_path)

    # resize image upload with PIL
    output_size = (125, 125)
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name