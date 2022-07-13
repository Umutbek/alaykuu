import uuid
import os

def all_image_file_path(instance, filename):
    """Generate file path for all image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/', filename)