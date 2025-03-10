import cloudinary
import cloudinary.uploader
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

def upload_file(file_path, folder=None):
    """
    Upload a file to Cloudinary and return the response
    """
    response = cloudinary.uploader.upload(
        file_path,
        folder=folder,
        resource_type="auto"
    )
    return response