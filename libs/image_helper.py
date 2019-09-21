import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import uuid
import glob

from minio import Minio
from minio.error import ResponseError

from flask_uploads import UploadSet, IMAGES, config_for_set, configure_uploads, patch_request_class

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def watermark_with_transparency(input_image_path: str = None,
                                output_image_path: str = None,
                                watermark_image_path: str = None,
                                isMobile: str = None) -> str:

    size = (1024, 768)
    original_image = Image.open(input_image_path)

    resize_image = original_image.resize(size)

    if isMobile == '1':
        angle = 270
        base_image = resize_image.rotate(angle, expand=True)
    else:
        base_image = resize_image;

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


def save_image_to_pdf(hyrf_id_prefix: str = None,
                      full_path_img2pdf: str = None,
                      MINIO_BUCKET_NAME: str =None,
                      MINIO_ENDPOINT: str = None,
                      MINIO_ACCESS_KEY: str = None,
                      MINIO_SECRET_KEY: str = None) -> str:

    file_extension = ".pdf"

    minioClient = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=None)

    objects = minioClient.list_objects(MINIO_BUCKET_NAME, prefix=hyrf_id_prefix, recursive=True)

    files = []
    for obj in objects:
        try:
            # file_full_path = r'.\\' + obj.object_name
            file_full_path = r"{}/{}".format(full_path_img2pdf, obj.object_name)
            files.append(obj.object_name)
            minioClient.fget_object(MINIO_BUCKET_NAME, obj.object_name, file_full_path)
        except ResponseError as err:
            print(err)

    images = []

    for f in files:
        file_full_path = r"{}/{}".format(full_path_img2pdf, f)
        im = Image.open(file_full_path)
        if im.mode == "RGBA":
            im = im.convert("RGB")
        images.append(im)

    minioFileName = "{}{}".format(uuid.uuid1().hex, file_extension)
    file_full_path_minio = "{}/{}".format(full_path_img2pdf, minioFileName)

    # Save file image to PDF
    images[0].save(file_full_path_minio, save_all=True, quality=100, append_images=images[1:])

    # Put file to minIO
    try:
        minioClient.fput_object(MINIO_BUCKET_NAME, minioFileName, file_full_path_minio, content_type='application/pdf')
    except ResponseError as err:
        return "Error {}".format(err)


    # Delete File
    exts = ['*.jpg', '*.pdf', '*.png']
    filelist = [f for ext in exts for f in glob.glob(os.path.join(full_path_img2pdf, ext))]

    for f in filelist:
        os.remove(f)

    return minioFileName


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
