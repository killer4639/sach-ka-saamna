import boto3, botocore

from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_REGION
from werkzeug.utils import secure_filename
s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def upload_file_to_s3(file, bucket_name=S3_BUCKET, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return file.filename

# only for uploading image function to S3. Nothing to do with preprocessing
def upload_file(imageFile):
    file = imageFile
    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

    # if no file name then select a file
    if file.filename == "":
        return "Please select a file"

    # D.
    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)
        return "https://" + S3_BUCKET + ".s3." + S3_REGION + ".amazonaws.com/" + output
    else:
        return null
