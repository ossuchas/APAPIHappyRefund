from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from minio import Minio
from minio.error import ResponseError
from PIL import Image as Img
from PIL import ImageDraw as ImgD
from PIL import ImageFont as ImgF

import traceback
import os
import base64
from datetime import timedelta

import uuid

from libs import image_helper
from libs.strings import errmsg
from schemas.image import ImageSchema
from schemas.crm_refund_docref import CrmRefundDocrefSchema
from models.crm_refund_docref import CrmRefundDocrefModel
from models.crm_contact_refund import CrmContactRefundModel

image_schema = ImageSchema()
docref_schema = CrmRefundDocrefSchema()

MINIO_ENDPOINT=os.environ.get("MINIO_ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME=os.environ.get("MINIO_BUCKET_NAME")
MINIO_FLAG=os.environ.get("MINIO_FLAG")
URL_PUBLIC_VIEW=os.environ.get("URL_PUBLIC_VIEW")


class ImageUpload(Resource):
    # @jwt_required
    def post(self):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        data = image_schema.load(request.files)
        _hyrf_id = request.form["hyrf"]
        _seqn_no = request.form["seqn_no"]
        _isMobile = request.form["isMobile"]
        folder = "customer"
        pdf_folder = "img2pdf"
        hyrf_id_prefix = "{}_".format(_hyrf_id)

        try:
            hyrf = CrmContactRefundModel.find_by_id(_hyrf_id)

            if not hyrf:
                return {"message": "Can not find Happy Refund ID"}, 404

            image_path = image_helper.save_image(data["image"], folder=folder)
            # here we only return the basename of the image and hide the internal folder structure from our user
            basename = image_helper.get_basename(image_path)
            img_type = image_helper.get_extension(image_path)

            full_path_img = f"static/images/{image_path}"
            full_path_img2pdf = r"static/images/{}".format(pdf_folder)
            with open(full_path_img, "rb") as img_file:
                img_file = base64.b64encode(img_file.read())

            # Watermark with transparency
            # Modified by Suchat S. 2019-12-04 Remove watermark
            # full_path_img_water = "static/images/customer/watermark_{}.png".format(hyrf.companyid)
            # image_helper.watermark_with_transparency(full_path_img, full_path_img, full_path_img_water, _isMobile)

            minioFileName = None
            minioUrl = None

            # Put an object image to MinIO
            if MINIO_FLAG == "Y":
                minioClient = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=None)
                # minioFileName = "{}_{}{}".format(uuid.uuid1().hex, _hyrf_id, img_type)
                minioFileName = "{}_{}{}".format(_hyrf_id, uuid.uuid1(), img_type)
                try:
                    minioClient.fput_object(MINIO_BUCKET_NAME, minioFileName, full_path_img, content_type='image/jpeg')
                    minioUrl = minioClient.presigned_get_object(MINIO_BUCKET_NAME, minioFileName, expires=timedelta(days=7))
                except ResponseError as err:
                    return {"message": errmsg("image_uploaded").format(err)}, 501

            img = CrmRefundDocrefModel(
                img_ref_contact_refund=_hyrf_id,
                img_name=basename,
                img_file=img_file,
                img_type=img_type,
                img_seqn=_seqn_no,
                minio_bucket_name=MINIO_BUCKET_NAME,
                minio_img_file_name=minioFileName,
                minio_img_url=minioUrl
            )
            try:
                img.save_to_db()
                # # img.exec_to_db()
                # pdf_file_name = image_helper.save_image_to_pdf(
                #     hyrf_id_prefix,
                #     full_path_img2pdf,
                #     MINIO_BUCKET_NAME,
                #     MINIO_ENDPOINT,
                #     MINIO_ACCESS_KEY,
                #     MINIO_SECRET_KEY
                # )
                #
                # # Update combile image to pdf
                # hyrf.doc_merge_url = r"{}{}".format(URL_PUBLIC_VIEW, pdf_file_name)
                # hyrf.save_to_db()
            except:
                return {"message": errmsg("image_uploaded").format(basename)}, 502

            return {"message": errmsg("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": errmsg("image_illegal_extension").format(extension)}, 400


class ImageMerge2PDF(Resource):
    def put(self, hyrf_id: int):
        pdf_folder = "img2pdf"
        hyrf_id_prefix = "{}_".format(hyrf_id)

        hyrf = CrmContactRefundModel.find_by_id(hyrf_id)

        if not hyrf:
            return {"message": "Can not find Happy Refund ID"}, 404

        full_path_img2pdf = r"static/images/{}".format(pdf_folder)

        try:
            pdf_file_name = image_helper.save_image_to_pdf(
                hyrf_id_prefix,
                full_path_img2pdf,
                MINIO_BUCKET_NAME,
                MINIO_ENDPOINT,
                MINIO_ACCESS_KEY,
                MINIO_SECRET_KEY )

            # Update combile image to pdf
            hyrf.doc_merge_url = r"{}{}".format(URL_PUBLIC_VIEW, pdf_file_name)
            hyrf.save_to_db()
        except:
            return {"message": errmsg("image_uploaded").format(full_path_img2pdf)}, 502

        return {"message": "Merge Image to PDF Success"}, 201
        # return hyrf_schema.dump(hyrf), 200


class Image(Resource):
    # @jwt_required
    def get(self, filename: str):
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        # user_id = get_jwt_identity()
        # folder = f"user_{user_id}"
        folder = "customer"
        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": errmsg("image_illegal_file_name").format(filename)}, 400
        try:
            # try to send the requested file to the user with status code 200
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": errmsg("image_not_found").format(filename)}, 404

    # @jwt_required
    def delete(self, filename: str):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to retrieve user information.
        """
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": errmsg("image_illegal_file_name").format(filename)}, 400

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": errmsg("image_deleted").format(filename)}, 200
        except FileNotFoundError:
            return {"message": errmsg("image_not_found").format(filename)}, 404
        except:
            traceback.print_exc()
            return {"message": errmsg("image_delete_failed")}, 500


class AvatarUpload(Resource):
    # @jwt_required
    def put(self):
        """
        This endpoint is used to upload user avatar. All avatars are named after the user's id
        in such format: user_{id}.{ext}.
        It will overwrite the existing avatar.
        """
        data = image_schema.load(request.files)
        filename = f"user_{get_jwt_identity()}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": errmsg("avatar_delete_failed")}, 500

        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext  # use our naming format + true extension
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {"message": errmsg("avatar_uploaded").format(basename)}, 200
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": errmsg("image_illegal_extension").format(extension)}, 400


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        This endpoint returns the avatar of the user specified by user_id.
        """
        folder = "avatars"
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            return send_file(avatar)
        return {"message": errmsg("avatar_not_found")}, 404
