"""
Cloudinary utility for file uploads
Handles PDF, image, and document uploads to Cloudinary cloud storage
"""
from typing import Optional
import cloudinary
import cloudinary.uploader
from app.config import settings

# Initialize Cloudinary configuration
def init_cloudinary():
    """Initialize Cloudinary with credentials from settings"""
    if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )

async def upload_to_cloudinary(
    file_content: bytes,
    filename: str,
    folder: str = "flowhive/minutes",
    resource_type: str = "auto"
) -> dict:
    """
    Upload a file to Cloudinary
    
    Args:
        file_content: The file content as bytes
        filename: Original filename
        folder: Cloudinary folder path
        resource_type: Type of resource ("auto", "image", "raw", "video")
    
    Returns:
        dict: Cloudinary response with URL, public_id, etc.
    """
    init_cloudinary()
    
    # Upload to Cloudinary
    result = cloudinary.uploader.upload(
        file_content,
        folder=folder,
        resource_type=resource_type,  # "auto" handles images, PDFs, docs
        use_filename=True,
        unique_filename=True,
        overwrite=False
    )
    
    return result

async def delete_from_cloudinary(public_id: str, resource_type: str = "auto") -> dict:
    """
    Delete a file from Cloudinary
    
    Args:
        public_id: The Cloudinary public_id of the file
        resource_type: Type of resource to delete
    
    Returns:
        dict: Cloudinary deletion response
    """
    init_cloudinary()
    
    result = cloudinary.uploader.destroy(
        public_id,
        resource_type=resource_type,
        invalidate=True
    )
    
    return result

def get_cloudinary_url(public_id: str, resource_type: str = "auto") -> str:
    """
    Generate a Cloudinary URL for a file
    
    Args:
        public_id: The Cloudinary public_id
        resource_type: Type of resource
    
    Returns:
        str: Full Cloudinary URL
    """
    init_cloudinary()
    
    if resource_type == "raw":
        return cloudinary.utils.cloudinary_url(
            public_id,
            resource_type="raw",
            secure=True,
            flags="attachment"
        )[0]
    
    return cloudinary.utils.cloudinary_url(
        public_id,
        secure=True
    )[0]
