import boto3
import botocore
import os
import uuid

BUCKET_NAME = os.environ.get("S3_BUCKET")
S3_LOCATION = f"https://{BUCKET_NAME}.s3.amazonaws.com/"
ALLOWED_EXTENSIONS = {"jpeg", "png", "gif", "jpg", "pdf"}

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get("S3_KEY"),
   aws_secret_access_key=os.environ.get("S3_SECRET")
)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_unique_filename(filename):
    ext = filename.rsplit(".", 1)[1].lower()
    unique_filename = uuid.uuid4().hex
    return f"{unique_filename}.{ext}"

def get_key_from_url(url):
    key = url.rsplit(".com/", 1)[1]
    key = key.replace("+", " ")
    return key

def upload_file_to_s3(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print(e,'FROM AWSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        # in case the our s3 upload fails
        return {"errors": str(e)}

    return {"url": f"{S3_LOCATION}{file.filename}"}



def delete_file_from_s3(url):
    try:
        s3.delete_object(Bucket='yelpclonehelp', Key=get_key_from_url(url))
        return {"message": "Succesfully deleted"}
    except Exception as e:
        return {"errors": str(e)}