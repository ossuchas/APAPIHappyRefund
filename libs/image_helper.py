import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from flask_uploads import UploadSet, IMAGES, config_for_set, configure_uploads, patch_request_class

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def watermark_with_transparency(input_image_path: str = None,
                                output_image_path: str = None,
                                watermark_image_path: str = None) -> str:

    size=(1024, 768)
    original_image = Image.open(input_image_path)

    base_image = original_image.resize(size)

    # base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size
    mark_width, mark_height = watermark.size
    position = (int((width / 2 - mark_width/ 2)), int((height / 2 - mark_height/ 2)))

    # transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(output_image_path)

    return


# def watermark_text(input_image_path, output_image_path, text, pos):
#     photo = Image.open(input_image_path)
#
#     # make the image editable
#     drawing = ImageDraw.Draw(photo)
#
#     black = (3, 8, 12)
#     font_path = "AP-Regular.ttf"
#     font = ImageFont.truetype(font_path, 30)
#
#     drawing.text(pos, text, fill=black, font=font)
#     # photo.show()
#     photo.save(output_image_path)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """
    Given a format-less filename, try to find the file by appending each of the allowed formats to the given
    filename and check if the file exists
    :param filename: formatless filename
    :param folder: the relative folder in which to search
    :return: the path of the image if exists, otherwise None
    """
    for _format in IMAGES:  # look for existing avatar and delete it
        avatar = f"{filename}.{_format}"
        avatar_path = IMAGE_SET.path(filename=avatar, folder=folder)
        if os.path.isfile(avatar_path):
            return avatar_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """
    Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """
    Check if a filename is secure according to our definition
    - starts with a-z A-Z 0-9 at least one time
    - only contains a-z A-Z 0-9 and _().-
    - followed by a dot (.) and a allowed_format at the end
    """
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)
    # format IMAGES into regex, eg: ('jpeg','png') --> 'jpeg|png'
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """
    Return file's basename, for example
    get_basename('some/folder/image.jpg') returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
