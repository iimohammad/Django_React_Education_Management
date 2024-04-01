import boto3
import logging
from botocore.exceptions import ClientError
import os
import dotenv
dotenv.read_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)

def cloud_storage(file_path, object_name):
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=os.environ.get('STORAGE_DOMAIN'),
            aws_access_key_id=os.environ.get('STORAGE_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('STORAGE_SECRET_ACCESS_KEY')
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = os.environ.get('bucket_name')
            bucket = s3_resource.Bucket(bucket_name)
            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
            logging.info("File uploaded successfully.")
            
            # Get object ACL
            object_acl = bucket.Object(object_name).Acl()
            logging.info(f"Old Object's ACL: {object_acl.grants}")
            
            # Update object's ACL
            object_acl.put(ACL='public-read')  # ACL='private'|'public-read'
            object_acl.reload()
            logging.info(f"New Object's ACL: {object_acl.grants}")
            
        except ClientError as e:
            logging.error(e)

script_dir = os.path.dirname(__file__)

# Example usage:
file_name = '1.jpg'
file_path = os.path.join(script_dir, file_name)
object_name = file_name
cloud_storage(file_path, object_name)