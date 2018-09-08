import base64

from io import BytesIO
import oss2

from config import settings
import time


def upload_img(img):
    auth = oss2.Auth(settings.OSS_KEY, settings.OSS_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_AREA, settings.OSS_BUCKET)
    img_name = str(int(time.time()*1000)) + '.png'
    result = bucket.put_object(settings.OSS_PATH + img_name, image_to_bytes(img))
    if result.status == 200:
        return img_name
    else:
        return None


def image_to_bytes(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='png')
    binary_data = output_buffer.getvalue()
    return binary_data
