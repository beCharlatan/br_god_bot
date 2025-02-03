import os
from minio import Minio
from minio.error import S3Error
import uuid
from io import BytesIO

class DocumentFilesStore:
    def __init__(self):
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")
        self.client = Minio(
            f"localhost:{os.getenv('MINIO_API_PORT')}",
            access_key=os.getenv("MINIO_ROOT_USER"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
            secure=False
        )
    
    def ensure_bucket(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Created bucket: {self.bucket_name}")
            return True
        except S3Error as exc:
            print(f"Error accessing MinIO: {exc}")
            return False

    def upload_image(self, image_data: bytes, filename: str) -> str | None:
        """Upload an image to MinIO storage and return its path"""
        try:
            # Ensure the bucket exists
            self.ensure_bucket()
            
            # Generate a unique object name
            object_name = f"images/{uuid.uuid4()}-{filename}"
            
            # Upload the image data
            self.client.put_object(
                self.bucket_name,
                object_name,
                BytesIO(image_data),
                len(image_data),
            )
            
            return object_name
        except S3Error as exc:
            print(f"Error uploading image: {exc}")
            return None

    def get_image_url(self, object_name: str) -> str:
        """Generate a presigned URL for accessing the image"""
        try:
            # Generate URL that expires in 7 days
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
            )
            return url
        except S3Error as exc:
            print(f"Error generating URL: {exc}")
            return ""